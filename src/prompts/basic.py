prompt_step_one = """{agent_description}
You are given a dialogue. You need to assess emotion of first speaker, estimate your confidence and give reasoning for your answer.
Your response should be in the following format:
`Emotion/Confidence/Reasoning`
For example: `Sad/0.5/The speaker implied that he is unsatisfied with his life`
The emotions can be happy, sad or angry.
Confidence estimation is a float number from 0 to 1.
Reasoning is a couple of sentences with reasons behind your answer.

The dialogue is following:
{dialog}
"""

simple_final_prompt = """You are the final judge over assessment of emotional condition of the speaker of the dialog above. 
Look at hints other agents provides you and construct a final answer.
Happiness says:
{happiness}
Anger says:
{anger}
Sadness says:
{sadness}
Fear says:
{fear}

`Emotion/Confidence/Reasoning`
For example: `Sad/0.5/The speaker implied that he is unsatisfied with his life`
The emotions can be happy, sad or angry.
Confidence estimation is a float number from 0 to 1.
Reasoning is a couple of sentences with reasons behind your answer. 
"""

prompt_step_two = """You are given a dialogue. You need to assess emotion of Speaker 1,
estimate your confidence and give reasoning for your answer.

Carefully review the following solutions from other agents as additional
information, and provide your own answer and step-by-step reasoning to
the question.
Clearly state which point of view you agree or disagree with and why.

The other agent answered the following:
Emotion: {}
Confidence: {}
Reasoning: {}

Your response should be in the following format:
Emotion Confidence Reasoning. For example: "Sad 0.5 The speaker
implied that he is unsatisfied with his life"
The emotions can be happy, sad or angry.
Confidence estimation is a float number from 0 to 1.
Reasoning is a couple of sentences with reasons behind your answer, reflect your opinion on other agent in it.

The dialogue is following:
Speaker 1: You could have done better, we did not hire you for lack of skills
Speaker 2: I will do better, I promise"""
