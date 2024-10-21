# InsideOut: Unifying Emotional LLMs to Foster Empathy
## Usage
#### Download Empathetic Dialogs dataset:

```bash
cd scripts
chmod +x download_data.sh
./download_data.sh
```
#### Install env:
```bash
conda env create -f environment.yaml
conda activate ec24
```
#### Run the script with the following command:
```bash
python script_name.py --setting <setting>
```
Replace <setting> with:
  - 1 for Setting One (ERC)
  - 2 for Setting Two (ERG)
  - b for the baseline setting

To modify settings use `configs` and `prompts` folder.

Pipeline of setting one is:
```
        # planner  ───> pass through───> simple_block ───>
        #  └───> insideout_block──> lambda ───└
```
For setting two: 
```
        # planner  ───> pass through──────────> insideout_block ───>
        #  └─> simple_block / tagger ──> lambda ───└
```

Train dialog length distribution (starting from 1 utterance):
`[2, 5, 20, 15135, 3421, 463, 218, 268]`

#### Run UI for assessors:
```bash
python -m assessor_ui.gradio.app
```


