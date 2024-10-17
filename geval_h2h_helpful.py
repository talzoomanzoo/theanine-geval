import argparse
import asyncio
import json
import os
import random
from copy import deepcopy

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio

TOTAL_COST = 0  # making this a global variable, be aware this may lead to issues in concurrent scenarios


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory_path", type= str, help='memory summary files for input')
    parser.add_argument("--input_paths", type=str, nargs= '+', help='List of input JSON files')
    parser.add_argument("--prompt", type=str,
                        default='./prompts/h2h_mem.txt')
    parser.add_argument("--save_dir", type=str, required=True,
                        help="It should be a NEW DIRECTORY. Please do not use an existing one")
    parser.add_argument("--num_sample", type=int, default=None,
                        help="If you want to test your code by sampling a small number of data, you can set this argument.")
    args = parser.parse_args()

    if args.num_sample:
        args.save_dir = args.save_dir + f"_sample{args.num_sample}"

    return args


def load_prompt(args):
    """
    Load .txt file as a prompt.
    """
    if args.prompt:
        with open(args.prompt, 'r') as f:
            prompt = f.read()
    return prompt


def prepare_model_input(prompt: str, data_paths: str, past_memories_path: str):
    '''
        input : prompt, data_paths (str)
        output : all_model_data (list of dict)
    '''
    with open(past_memories_path, 'r') as json_file:
        memory_data = json.load(json_file)
    
    data1, data2 = None, None
    for idx, data_path in enumerate(data_paths):
        print(f"Loading data from {data_path} for translation...")
        with open(data_path, 'r') as json_file:
            data = json.load(json_file)
            if idx == 0:
                data1 = data
            elif idx == 1:
                data2 = data

    all_model_data = []
    for i in range(len(data1)):
        input_temp = dict()
        input_temp['id'] = i
        
        input_temp['model_input'] = prompt.format(**{
            "current_dialogue": data1[i]['current_dialogue'],
            "speaker": data[i]['speaker'],
            "previous_summary": data1[i]['previous_summary'],
            "memory1": data1[i]['memory_text'],
            "memory2": data2[i]['memory_text']
        })
        
        # for key in data1[i].keys():
        #     input_temp[key] = data1[i][key]
        
        all_model_data.append(input_temp)
            
    return all_model_data


def prepare_dialogue(dialogue_list):
    processed_turns = []
    for i in range(len(dialogue_list)):
        turn_text = f"{dialogue_list[i]['role']}: {dialogue_list[i]['message']}"
        processed_turns.append(turn_text)
    return "\n".join(processed_turns)


def load_and_prepare_data(args):
    prompt = load_prompt(args)
    print("Preparing model inputs...")

    all_model_data = prepare_model_input(
        prompt, args.input_paths, args.memory_path)
    return all_model_data


def sample_indices(all_model_inputs, num_sample):
    # random.seed(0)
    # cand_indices = list(range(len(all_model_inputs)))
    # sampled_indices = random.sample(cand_indices, num_sample)
    sampled_indices = list(range(min(num_sample, len(all_model_inputs))))
    return sampled_indices


def filter_data(all_model_data, num_sample):
    if num_sample:
        sampled_indices = sample_indices(all_model_data, num_sample)
        all_model_data = [all_model_data[i] for i in sampled_indices]
    return all_model_data


async def async_generate(llm, model_data, idx, save_dir):
    global TOTAL_COST
    system_message = SystemMessage(content=model_data['model_input'])
    while True:
        try:
            response = await llm.agenerate([[system_message]])
            token_used = response.llm_output['token_usage']['total_tokens']
            TOTAL_COST += token_used / 1000 * 0.002
            print(idx, TOTAL_COST)
            break
        except Exception as e:
            print(f"Exception occurred: {e}")

    result = deepcopy(model_data)
    result['prediction'] = response.generations[0][0].text
    with open(os.path.join(save_dir, f"{idx}.json"), "w",
              encoding='UTF-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    return result


async def generate_concurrently(all_model_data, start_idx, save_dir):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables. Please set OPENAI_API_KEY.")
    
    llm = ChatOpenAI(
        model_name='gpt-4o',  # 'gpt-4o-mini' or 'gpt-4o'
        temperature=1.0,
        max_tokens=1500,
        max_retries=100,
        openai_api_key=api_key  # Explicitly passing the API key
    )
    
    # tasks = [async_generate(llm, model_data, i + start_idx, save_dir)
    #          for i, model_data in enumerate(all_model_data)]

    # return await tqdm_asyncio.gather(*tasks)
    
    tasks = []
    for i, model_data in enumerate(all_model_data):
        output_file_path = os.path.join(save_dir, f"{i + start_idx}.json")
        if os.path.exists(output_file_path):
            print(f"Skipping {output_file_path}, already exists.")
            continue  # Skip if the file already exists

        tasks.append(async_generate(llm, model_data, i + start_idx, save_dir))

    if tasks:  # Only gather if there are tasks to avoid errors
        return await tqdm_asyncio.gather(*tasks)
    else:
        print("No new files to generate.")
        return []


async def main(args):
    all_model_data = load_and_prepare_data(args)
    
    if args.num_sample is not None:
        all_model_data = filter_data(all_model_data, args.num_sample)

    if os.path.exists(args.save_dir):
        print("The save_dir already exists. Please change the save_dir.")

    os.makedirs(args.save_dir, exist_ok=True)
    all_results = []
    if len(all_model_data) > 300:
        for start_idx in tqdm(range(0, len(all_model_data), 300)):
            cur_model_data = all_model_data[start_idx:start_idx + 300]
            all_results.extend(
                await generate_concurrently(cur_model_data, start_idx,
                                            args.save_dir))
    else:
        all_results = await generate_concurrently(all_model_data, 0,
                                                  args.save_dir)

    # total_result_path = args.save_dir + "_total_results.json"
    # with open(os.path.join(total_result_path), "w", encoding='UTF-8') as f:
    #     json.dump(all_results, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args))