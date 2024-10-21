import os
import openai
from dotenv import load_dotenv
from tqdm import tqdm
import argparse

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


def main(setting_choice, limit):
    dataset = EmpDialogsDataset(
        "test", data_folder="data/empatheticdialogues", cut_n_last=1
    )

    if str(setting_choice) == "1":
        current_setting = SettingOneAssembler("configs/setting1.json").assemble()
    elif str(setting_choice) == "2":
        current_setting = SettingTwoAssembler("configs/setting2.json").assemble()
    elif setting_choice == "berc":
        current_setting = assemble_baseline("configs/baseline_ERC.json")
    elif setting_choice == "bemp":
        current_setting = assemble_baseline("configs/baseline_EMP.json")
    elif setting_choice == "ins_erc":
        current_setting = SettingOneAssembler("configs/setting1.json").insideout_block
    else:
        raise ValueError(f"Invalid setting choice: {setting_choice}")

    for i, inp in tqdm(enumerate(dataset)):
        logger.info(f"New input:\n{inp}")
        current_setting.invoke({"dialog": inp})
        if limit is not None and i + 1 >= limit:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run dialog system with selected setting"
    )
    parser.add_argument(
        "--setting",
        "-s",
        type=str,
        choices=["1", "2", "berc", "bemp", "ins_erc"],
        required=True,
        help="Select the setting to use: 1 for Setting One, 2 for Setting Two, 'berc' or 'bemp' for the baseline setting.",
    )

    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        help="Limits number of elements from a dataset.",
    )

    args = parser.parse_args()
    main(setting_choice=args.setting, limit=args.limit)
