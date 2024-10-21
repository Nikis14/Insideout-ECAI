import os
import openai
from dotenv import load_dotenv
from tqdm import tqdm
import argparse
import gradio as gr
from functools import partial


from src.datasets.empathetic_dialogs import EmpDialogsDataset
from src.logging_utils import get_logger
from src.agents.full_settings import (
    SettingOneAssembler,
    SettingTwoAssembler,
    assemble_baseline,
)

logger = get_logger(__name__, to_file=True)
load_dotenv(".env")
assert "OPENAI_API_KEY" in os.environ
openai.api_key = os.environ["OPENAI_API_KEY"]



s1 = SettingOneAssembler("configs/setting1.json").assemble()
s2 = SettingTwoAssembler("configs/setting2.json").assemble()
b = assemble_baseline("configs/baseline_EMP.json")


s1_4 = SettingOneAssembler("configs/4/setting1.json").assemble()
s2_4 = SettingTwoAssembler("configs/4/setting2.json").assemble()
b_4 = assemble_baseline("configs/4/baseline_EMP.json")


def transform_to_dialog(message, chat_history):
    dialog = ""
    for messages in chat_history:
        dialog += f"Speaker 1: {messages[0]}\nSpeaker 2: {messages[1]}\n"
    dialog += f"Speaker 1: {message}"
    return dialog

def respond(message, chat_history, model):
    print(chat_history)
    print()
    dialog = transform_to_dialog(message, chat_history)
    bot_message = model.invoke({"dialog": dialog})
    #print(bot_message)
    if isinstance(bot_message, list):
        bot_message = bot_message[0]
    bot_message = bot_message.strip("Speaker 2: ")
    #print(bot_message)
    chat_history.append((message, bot_message))
    return "", chat_history

base_respond = partial(respond, model = b)
setting1_respond = partial(respond, model = s1)
setting2_respond = partial(respond, model = s2)

base_respond_4 = partial(respond, model = b_4)
setting1_respond_4 = partial(respond, model = s1_4)
setting2_respond_4 = partial(respond, model = s2_4)

dataset = EmpDialogsDataset(
    "test", data_folder="data/empatheticdialogues", cut_n_last=1
)



idx = 10
dialogs = []

def get_dialog(idx, dataset=dataset, funcs = [b, s1, s2]):
    datum = dataset[idx]
    speaker_1 = [el.strip("Speaker 1: ") for el in datum.split('\n')[::2]]
    speaker_2 = [el.strip("Speaker 2: ") for el in datum.split('\n')[1::2]]
    outs = []
    for func in funcs:
        bot_message = func.invoke({"dialog": datum})
        if isinstance(bot_message, list):
            bot_message = bot_message[0]
        bot_message = bot_message.strip("Speaker 2: ")
        speaker_2.append(bot_message)
        outs.append(list(zip(speaker_1, speaker_2)))
        speaker_2.pop()

    return outs

get_dialog_4 = partial(get_dialog, funcs = [b_4, s1_4, s2_4])

with gr.Blocks() as demo:
    with gr.Tab("Eval: GPT 3.5"):
        with gr.Row():
            text1 = gr.Chatbot(label="Baseline", likeable=True, height=600)
            text2 = gr.Chatbot(label="Setting 1", likeable=True, height=600)
            text3 = gr.Chatbot(label="Setting 2", likeable=True, height=600)
        msg1 = gr.Textbox(label="Input")
        with gr.Row():
            clear = gr.ClearButton([msg1, text1, text2, text3])
            next = gr.Button("Submit")
            how_many = gr.Number(value=0)
            # dialog_text = gr.Textbox(label="DT", max_lines=2, interactive=False, visible=False)
            next.click(get_dialog, inputs=[how_many], outputs=[text1, text2, text3])

    with gr.Tab("Eval: GPT 4"):
        with gr.Row():
            text1_4 = gr.Chatbot(label="Baseline", likeable=True, height=600)
            text2_4 = gr.Chatbot(label="Setting 1", likeable=True, height=600)
            text3_4 = gr.Chatbot(label="Setting 2", likeable=True, height=600)
        msg1_4 = gr.Textbox(label="Input")
        with gr.Row():
            clear = gr.ClearButton([msg1_4, text1_4, text2_4, text3_4])
            next = gr.Button("Submit")
            how_many_4 = gr.Number(value=0)
            # dialog_text = gr.Textbox(label="DT", max_lines=2, interactive=False, visible=False)
            next.click(get_dialog_4, inputs=[how_many_4], outputs=[text1_4, text2_4, text3_4])

    with gr.Tab("Chat: GPT 3.5"):
        with gr.Row():
            chatbot1 = gr.Chatbot(label="Baseline", likeable=True, height=600)
            chatbot2 = gr.Chatbot(label="Setting 1", likeable=True, height=600)
            chatbot3 = gr.Chatbot(label="Setting 2", likeable=True, height=600)
        msg = gr.Textbox(label="Input")
        clear = gr.ClearButton([msg, chatbot1, chatbot2, chatbot3])

        msg.submit(base_respond, [msg, chatbot1], [msg, chatbot1])
        msg.submit(setting1_respond, [msg, chatbot2], [msg, chatbot2])
        msg.submit(setting2_respond, [msg, chatbot3], [msg, chatbot3])
    with gr.Tab("Chat: GPT 4"):
        with gr.Row():
            chatbot1_4 = gr.Chatbot(label="Baseline", likeable=True, height=600)
            chatbot2_4 = gr.Chatbot(label="Setting 1", likeable=True, height=600)
            chatbot3_4 = gr.Chatbot(label="Setting 2", likeable=True, height=600)
        msg_4 = gr.Textbox(label="Input")
        clear_4 = gr.ClearButton([msg_4, chatbot1_4, chatbot2_4, chatbot3_4])

        msg_4.submit(base_respond_4, [msg_4, chatbot1_4], [msg_4, chatbot1_4])
        msg_4.submit(setting1_respond_4, [msg_4, chatbot2_4], [msg_4, chatbot2_4])
        msg_4.submit(setting2_respond_4, [msg_4, chatbot3_4], [msg_4, chatbot3_4])

demo.launch(height=900, share=True)