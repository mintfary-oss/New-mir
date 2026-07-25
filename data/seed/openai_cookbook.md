=== openai-cookbook/README.md ===
<a href="https://cookbook.openai.com" target="_blank">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="/images/openai-cookbook-white.png" style="max-width: 100%; width: 400px; margin-bottom: 20px">
    <img alt="OpenAI Cookbook Logo" src="/images/openai-cookbook.png" width="400px">
  </picture>
</a>

<h3></h3>
 
> ✨ Navigate at [cookbook.openai.com](https://cookbook.openai.com)

Example code and guides for accomplishing common tasks with the [OpenAI API](https://platform.openai.com/docs/introduction). To run these examples, you'll need an OpenAI account and associated API key ([create a free account here](https://platform.openai.com/signup)). Set an environment variable called `OPENAI_API_KEY` with your API key. Alternatively, in most IDEs such as Visual Studio Code, you can create an `.env` file at the root of your repo containing `OPENAI_API_KEY=<your API key>`, which will be picked up by the notebooks.

Most code examples are written in Python, though the concepts can be applied in any language.

For other useful tools, guides and courses, check out these [related resources from around the web](https://cookbook.openai.com/related_resources).

## License

MIT License

=== articles/how_to_work_with_large_language_models.md ===
# How to work with large language models

## How large language models work

[Large language models][Large language models Blog Post] are functions that map text to text. Given an input string of text, a large language model predicts the text that should come next.

The magic of large language models is that by being trained to minimize this prediction error over vast quantities of text, the models end up learning concepts useful for these predictions. For example, they learn:

- how to spell
- how grammar works
- how to paraphrase
- how to answer questions
- how to hold a conversation
- how to write in many languages
- how to code
- etc.

They do this by “reading” a large amount of existing text and learning how words tend to appear in context with other words, and uses what it has learned to predict the next most likely word that might appear in response to a user request, and each subsequent word after that.

GPT-3 and GPT-4 power [many software products][OpenAI Customer Stories], including productivity apps, education apps, games, and more.

## How to control a large language model

Of all the inputs to a large language model, by far the most influential is the text prompt.

Large language models can be prompted to produce output in a few ways:

- **Instruction**: Tell the model what you want
- **Completion**: Induce the model to complete the beginning of what you want
- **Scenario**: Give the model a situation to play out
- **Demonstration**: Show the model what you want, with either:
  - A few examples in the prompt
  - Many hundreds or thousands of examples in a fine-tuning training dataset

An example of each is shown below.

### Instruction prompts

Write your instruction at the top of the prompt (or at the bottom, or both), and the model will do its best to follow the instruction and then stop. Instructions can be detailed, so don't be afraid to write a paragraph explicitly detailing the output you want, just stay aware of how many [tokens](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them) the model can process.

Example instruction prompt:

```text
Extract the name of the author from the quotation below.

“Some humans theorize that intelligent species go extinct before they can expand into outer space. If they're correct, then the hush of the night sky is the silence of the graveyard.”
― Ted Chiang, Exhalation
```

Output:

```text
Ted Chiang
```

### Completion prompt example

Completion-style prompts take advantage of how large language models try to write text they think is most likely to come next. To steer the model, try beginning a pattern or sentence that will be completed by the output you want to see. Relative to direct instructions, this mode of steering large language models can take more care and experimentation. In addition, the models won't necessarily know where to stop, so you will often need stop sequences or post-processing to cut off text generated beyond the desired output.

Example completion prompt:

```text
“Some humans theorize that intelligent species go extinct before they can expand into outer space. If they're correct, then the hush of the night sky is the silence of the graveyard.”
― Ted Chiang, Exhalation

The author of this quote is
```

Output:

```text
 Ted Chiang
```

### Scenario prompt example

Giving the model a scenario to follow or role to play out can be helpful for complex queries or when seeking imaginative responses. When using a hypothetical prompt, you set up a situation, problem, or story, and then ask the model to respond as if it were a character in that scenario or an expert on the topic.

Example scenario prompt:

```text
Your role is to extract the name of the author from any given text

“Some humans theorize that intelligent species go extinct before they can expand into outer space. If they're correct, then the hush of the night sky is the silence of the graveyard.”
― Ted Chiang, Exhalation
```

Output:

```text
 Ted Chiang
```

### Demonstration prompt example (few-shot learning)

Similar to completion-style prompts, demonstrations can show the model what you want it to do. This approach is sometimes called few-shot learning, as the model learns from a few examples provided in the prompt.

Example demonstration prompt:

```text
Quote:
“When the reasoning mind is forced to confront the impossible again and again, it has no choice but to adapt.”
― N.K. Jemisin, The Fifth Season
Author: N.K. Jemisin

Quote:
“Some humans theorize that intelligent species go extinct before they can expand into outer space. If they're correct, then the hush of the night sky is the silence of the graveyard.”
― Ted Chiang, Exhalation
Author:
```

Output:

```text
 Ted Chiang
```

### Fine-tuned prompt example

With enough training examples, you can [fine-tune][Fine Tuning Docs] a custom model. In this case, instructions become unnecessary, as the model can learn the task from the training data provided. However, it can be helpful to include separator sequences (e.g., `->` or `###` or any string that doesn't commonly appear in your inputs) to tell the model when the prompt has ended and the output should begin. Without separator sequences, there is a risk that the model continues elaborating on the input text rather than starting on the answer you want to see.

Example fine-tuned prompt (for a model that has been custom trained on similar prompt-completion pairs):

```text
“Some humans theorize that intelligent species go extinct before they can expand into outer space. If they're correct, then the hush of the night sky is the silence of the graveyard.”
― Ted Chiang, Exhalation

###


```

Output:

```text
 Ted Chiang
```

## Code Capabilities

Large language models aren't only great at text - they can be great at code too. OpenAI's [GPT-4][GPT-4 and GPT-4 Turbo] model is a prime example.

GPT-4 powers [numerous innovative products][OpenAI Customer Stories], including:

- [GitHub Copilot] (autocompletes code in Visual Studio and other IDEs)
- [Replit](https://replit.com/) (can complete, explain, edit and generate code)
- [Cursor](https://cursor.sh/) (build software faster in an editor designed for pair-programming with AI)

GPT-4 is more advanced than previous models like `gpt-3.5-turbo-instruct`. But, to get the best out of GPT-4 for coding tasks, it's still important to give clear and specific instructions. As a result, designing good prompts can take more care.

### More prompt advice

For more prompt examples, visit [OpenAI Examples][OpenAI Examples].

In general, the input prompt is the best lever for improving model outputs. You can try tricks like:

- **Be more specific** E.g., if you want the output to be a comma separated list, ask it to return a comma separated list. If you want it to say "I don't know" when it doesn't know the answer, tell it 'Say "I don't know" if you do not know the answer.' The more specific your instructions, the better the model can respond.
- **Provide Context**: Help the model understand the bigger picture of your request. This could be background information, examples/demonstrations of what you want or explaining the purpose of your task.
- **Ask the model to answer as if it was an expert.** Explicitly asking the model to produce high quality output or output as if it was written by an expert can induce the model to give higher quality answers that it thinks an expert would write. Phrases like "Explain in detail" or "Describe step-by-step" can be effective.
- **Prompt the model to write down the series of steps explaining its reasoning.** If understanding the 'why' behind an answer is important, prompt the model to include its reasoning. This can be done by simply adding a line like "[Let's think step by step](https://arxiv.org/abs/2205.11916)" before each answer.

[Fine Tuning Docs]: https://platform.openai.com/docs/guides/fine-tuning
[OpenAI Customer Stories]: https://openai.com/customer-stories
[Large language models Blog Post]: https://openai.com/research/better-language-models
[GitHub Copilot]: https://github.com/features/copilot/
[GPT-4 and GPT-4 Turbo]: https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
[GPT3 Apps Blog Post]: https://openai.com/blog/gpt-3-apps/
[OpenAI Examples]: https://platform.openai.com/examples

=== articles/techniques_to_improve_reliability.md ===
# Techniques to improve reliability

When GPT-3 fails on a task, what should you do?

- Search for a better prompt that elicits more reliable answers?
- Invest in thousands of examples to fine-tune a custom model?
- Assume the model is incapable of the task, and move on?

There is no simple answer - it depends. However, if your task involves logical reasoning or complexity, consider trying the techniques in this article to build more reliable, high-performing prompts.

## Why GPT-3 fails on complex tasks

If you were asked to multiply 13 by 17, would the answer pop immediately into your mind? For most of us, probably not. Yet, that doesn't mean humans are incapable of two-digit multiplication. With a few seconds, and some pen and paper, it's not too taxing to work out that 13 x 17 = 130 + 70 + 21 = 221.

Similarly, if you give GPT-3 a task that's too complex to do in the time it takes to calculate its next token, it may confabulate an incorrect guess. Yet, akin to humans, that doesn't necessarily mean the model is incapable of the task. With some time and space to reason things out, the model still may be able to answer reliably.

As an example, if you ask `gpt-3.5-turbo-instruct` the following math problem about juggling balls, it answers incorrectly:

```gpt-3.5-turbo-instruct
Q: A juggler has 16 balls. Half of the balls are golf balls and half of the golf balls are blue. How many blue golf balls are there?
A:
```

```gpt-3.5-turbo-instruct
There are 8 blue golf balls.
```

Does this mean that GPT-3 cannot do simple math problems? No; in fact, it turns out that by prompting the model with `Let's think step by step`, the model solves the problem reliably:

```gpt-3.5-turbo-instruct
Q: A juggler has 16 balls. Half of the balls are golf balls and half of the golf balls are blue. How many blue golf balls are there?
A: Let's think step by step.
```

```gpt-3.5-turbo-instruct
There are 16 balls in total.
Half of the balls are golf balls.
That means that there are 8 golf balls.
Half of the golf balls are blue.
That means that there are 4 blue golf balls.
```

Of course, it's hard to tell from only a single example whether this `Let's think step by step` trick actually works in general or just got lucky on this particular problem. But it really does work. On a benchmark of word math problems, the `Let's think step by step` trick raised GPT-3's solve rate massively, from a worthless 18% to a decent 79%!

## Model capabilities depend on context

When learning to work with GPT-3, one common conceptual mistake is to believe that its capabilities are fixed across all contexts. E.g., if GPT-3 gets a simple logic question wrong, then it must be incapable of simple logic.

But as the `Let's think step by step` example illustrates, apparent failures of GPT-3 can sometimes be remedied with a better prompt that helps the model steer itself toward the correct output.

## How to improve reliability on complex tasks

The rest of this article shares techniques for improving reliability of large language models on complex tasks. Although some of the techniques are specific to certain types of problems, many of them are built upon general principles that can be applied to a wide range of tasks, e.g.:

- Give clearer instructions
- Split complex tasks into simpler subtasks
- Structure the instruction to keep the model on task
- Prompt the model to explain before answering
- Ask for justifications of many possible answers, and then synthesize
- Generate many outputs, and then use the model to pick the best one
- Fine-tune custom models to maximize performance

## Split complex tasks into simpler tasks

One way to give a model more time and space to think is to break tasks into simpler pieces.

As an example, consider a task where we ask the model a multiple-choice question about some text - in this case, a game of Clue. When asked directly, `gpt-3.5-turbo-instruct` isn't able to put clues 3 & 5 together, and answers incorrectly:

```gpt-3.5-turbo-instruct
Use the following clues to answer the following multiple-choice question.

Clues:
1. Miss Scarlett was the only person in the lounge.
2. The person with the pipe was in the kitchen.
3. Colonel Mustard was the only person in the observatory.
4. Professor Plum was not in the library nor the billiard room.
5. The person with the candlestick was in the observatory.

Question: Was Colonel Mustard in the observatory with the candlestick?
(a) Yes; Colonel Mustard was in the observatory with the candlestick
(b) No; Colonel Mustard was not in the observatory with the candlestick
(c) Unknown; there is not enough information to determine whether Colonel Mustard was in the observatory with the candlestick

Solution:
```

```gpt-3.5-turbo-instruct
(c) Unknown; there is not enough information to determine whether Colonel Mustard was in the observatory with the candlestick
```

Although clues 3 and 5 establish that Colonel Mustard was the only person in the observatory and that the person in the observatory had the candlestick, the model fails to combine them into a correct answer of (a) Yes.

However, instead of asking for the answer directly, we can split the task into three pieces:

- First, go through the clues one by one and consider whether the clue is potentially relevant
- Second, combine the relevant clues to reason out the answer to the question
- Third, write the final answer: either (a), (b), or (c)

```gpt-3.5-turbo-instruct
Use the following clues to answer the following multiple-choice question, using the following procedure:
(1) First, go through the clues one by one and consider whether the clue is potentially relevant
(2) Second, combine the relevant clues to reason out the answer to the question
(3) Third, map the answer to one of the multiple choice answers: either (a), (b), or (c)

Clues:
1. Miss Scarlett was the only person in the lounge.
2. The person with the pipe was in the kitchen.
3. Colonel Mustard was the only person in the observatory.
4. Professor Plum was not in the library nor the billiard room.
5. The person with the candlestick was in the observatory.

Question: Was Colonel Mustard in the observatory with the candlestick?
(a) Yes; Colonel Mustard was in the observatory with the candlestick
(b) No; Colonel Mustard was not in the observatory with the candlestick
(c) Unknown; there is not enough information to determine whether Colonel Mustard was in the observatory with the candlestick

Solution:
(1) First, go through the clues one by one and consider whether the clue is potentially relevant:
```

```gpt-3.5-turbo-instruct
Clue 1: Miss Scarlett was the only person in the lounge. This clue is not relevant.
Clue 2: The person with the pipe was in the kitchen. This clue is not relevant.
Clue 3: Colonel Mustard was the only person in the observatory. This clue is relevant.
Clue 4: Professor Plum was not in the library nor the billiard room. This clue is not relevant.
Clue 5: The person with the candlestick was in the observatory. This clue is relevant.

(2) Second, combine the relevant clues to reason out the answer to the question:
Clue 3 and Clue 5 both say that the person with the candlestick was in the observatory. Colonel Mustard was the only person in the observatory, so Colonel Mustard was the person with the candlestick.

(3) Third, write the final answer:
(a) Yes; Colonel Mustard was in the observatory with the candlestick
```

By giving the model more time and space to think, and guiding it along a reasoning plan, it's able to figure out the correct answer of (a) Yes.

Another benefit of splitting complex instructions into smaller subtasks is that it can help keep the model focused on each subtask.

For example, if we ask `gpt-3.5-turbo-instruct` to summarize a text in its original language, the model can lapse back into English:

```gpt-3.5-turbo-instruct
Summarize the text using the original language of the text. The summary should be one sentence long.

Text:
"""
La estadística (la forma femenina del término alemán Statistik, derivado a su vez del italiano statista, "hombre de Estado")​ es una ciencia que estudia la variabilidad, colección, organización, análisis, interpretación, y presentación de los datos, así como el proceso aleatorio que los genera siguiendo las leyes de la probabilidad.​ La estadística es una ciencia formal deductiva, con un conocimiento propio, dinámico y en continuo desarrollo obtenido a través del método científico formal. En ocasiones, las ciencias fácticas necesitan utilizar técnicas estadísticas durante su proceso de investigación factual, con el fin de obtener nuevos conocimientos basados en la experimentación y en la observación. En estos casos, la aplicación de la estadística permite el análisis de datos provenientes de una muestra representativa, que busca explicar las correlaciones y dependencias de un fenómeno físico o natural, de ocurrencia en forma aleatoria o condicional.
"""

Summary:
```

```gpt-3.5-turbo-instruct
The text explains that statistics is a science that studies the variability, collection, organization, analysis, interpretation, and presentation of data, as well as the random process that generates them following the laws of probability.
```

However, if we first ask the model to identify the language of the text, and then summarize the text, it becomes more reliable:

```gpt-3.5-turbo-instruct
First, identify the language of the text. Second, summarize the text using the original language of the text. The summary should be one sentence long.

Text:
"""
La estadística (la forma femenina del término alemán Statistik, derivado a su vez del italiano statista, "hombre de Estado")​ es una ciencia que estudia la variabilidad, colección, organización, análisis, interpretación, y presentación de los datos, así como el proceso aleatorio que los genera siguiendo las leyes de la probabilidad.​ La estadística es una ciencia formal deductiva, con un conocimiento propio, dinámico y en continuo desarrollo obtenido a través del método científico formal. En ocasiones, las ciencias fácticas necesitan utilizar técnicas estadísticas durante su proceso de investigación factual, con el fin de obtener nuevos conocimientos basados en la experimentación y en la observación. En estos casos, la aplicación de la estadística permite el análisis de datos provenientes de una muestra representativa, que busca explicar las correlaciones y dependencias de un fenómeno físico o natural, de ocurrencia en forma aleatoria o condicional.
"""

Language:
```

```gpt-3.5-turbo-instruct
Spanish

La estadística es una ciencia que estudia la variabilidad, colección, organización, análisis, interpretación, y presentación de los datos, así como el proceso aleatorio que los genera siguiendo las leyes de la probabilidad.
```

## Prompt the model to explain before answering

Another powerful technique for improving the reliability of answers is to prompt the model to gradually reason out the answer rather than jumping immediately to the final answer. By 'thinking aloud' the model can be far more likely to arrive at the correct answer.

### Zero-shot

#### Method

Published by [Takeshi Kojima et al. in 2022](https://arxiv.org/abs/2205.11916), the easiest way to prompt a model to reason out the answer is to simply prepend answers with `Let's think step by step.` Figure 2 illustrates an example:

[![zero-shot reasoning example](/images/zero-shot_reasoners_fig2.png)
<br>Source: _Large Language Models are Zero-Shot Reasoners_ by Takeshi Kojima et al. (2022).](https://arxiv.org/abs/2205.11916)

#### Results

Applying this simple trick to the MultiArith math dataset, the authors found `Let's think step by step` quadrupled the accuracy, from 18% to 79%!

[![zero-shot reasoning example](/images/zero-shot_reasoners_tab5.png)
<br>Source: _Large Language Models are Zero-Shot Reasoners_ by Takeshi Kojima et al. (2022).](https://arxiv.org/abs/2205.11916)

#### Implications

Although the `Let's think step by step` trick works well on math problems, it's not effective on all tasks. The authors found that it was most helpful for multi-step arithmetic problems, symbolic reasoning problems, strategy problems, and other reasoning problems. It didn't help with simple math problems or common sense questions, and presumably wouldn't help with many other non-reasoning tasks either.

[![zero-shot reasoning example](/images/zero-shot_reasoners_tab1.png)
<br>Source: _Large Language Models are Zero-Shot Reasoners_ by Takeshi Kojima et al. (2022).](https://arxiv.org/abs/2205.11916)

To learn more, read the [full paper](https://arxiv.org/abs/2205.11916).

If you apply this technique to your own tasks, don't be afraid to experiment with customizing the instruction. `Let's think step by step` is rather generic, so you may find better performance with instructions that hew to a stricter format customized to your use case. For example, you can try more structured variants like `First, think step by step about why X might be true. Second, think step by step about why Y might be true. Third, think step by step about whether X or Y makes more sense.`. And you can even give the model an example format to help keep it on track, e.g.:

```gpt-3.5-turbo-instruct
Using the IRS guidance below, answer the following questions using this format:
(1) For each criterion, determine whether it is met by the vehicle purchase
- {Criterion} Let's think step by step. {explanation} {yes or no, or if the question does not apply then N/A}.
(2) After considering each criterion in turn, phrase the final answer as "Because of {reasons}, the answer is likely {yes or no}."

IRS guidance:
"""
You may be eligible for a federal tax credit under Section 30D if you purchased a car or truck that meets the following criteria:
- Does the vehicle have at least four wheels?
- Does the vehicle weigh less than 14,000 pounds?
- Does the vehicle draw energy from a battery with at least 4 kilowatt hours that may be recharged from an external source?
- Was the vehicle purchased in a year before 2022?
  - If so, has the manufacturer sold less than 200,000 qualifying vehicles? (Tesla and GM have sold more than 200,000 qualifying vehicles.)
- Was the vehicle purchased in a year after 2022?
  - If so, is the vehicle present in the following list of North American-assembled vehicles? (The only electric vehicles assembled in North America are the Audi Q5, BMW 330e, BMW X5, Chevrolet Bolt EUV, Chevrolet Bolt EV, Chrysler Pacifica PHEV, Ford Escape PHEV, Ford F Series, Ford Mustang MACH E, Ford Transit Van, GMC Hummer Pickup, GMC Hummer SUV, Jeep Grand Cherokee PHEV, Jeep Wrangler PHEV, Lincoln Aviator PHEV, Lincoln Corsair Plug-in, Lucid Air, Nissan Leaf, Rivian EDV, Rivian R1S, Rivian R1T, Tesla Model 3, Tesla Model S, Tesla Model X, Tesla Model Y, Volvo S60, BMW 330e, Bolt EV, Cadillac Lyriq, Mercedes EQS SUV, and Nissan Leaf.)
"""

Question: Can I claim a federal tax credit for my Toyota Prius Prime bought in 2021?

Solution:

(1) For each criterion, determine whether it is met by the vehicle purchase
- Does the vehicle have at least four wheels? Let's think step by step.
```

```gpt-3.5-turbo-instruct
 The Toyota Prius Prime has four wheels, so the answer is yes.
- Does the vehicle weigh less than 14,000 pounds? Let's think step by step. The Toyota Prius Prime weighs less than 14,000 pounds, so the answer is yes.
- Does the vehicle draw energy from a battery with at least 4 kilowatt hours that may be recharged from an external source? Let's think step by step. The Toyota Prius Prime has a battery with at least 4 kilowatt hours that may be recharged from an external source, so the answer is yes.
- Was the vehicle purchased in a year before 2022? Let's think step by step. The Toyota Prius Prime was purchased in 2021, which is before 2022, so the answer is yes.
- Was the vehicle purchased in a year after 2022? N/A
- If so, is the vehicle present in the following list of North American-assembled vehicles? N/A

(2) After considering each criterion in turn, phrase the final answer as "Because of {reasons}, the answer is likely {yes or no}."

Because the Toyota Prius Prime meets all of the criteria for a federal tax credit, the answer is likely yes.
```

### Few-shot examples

#### Method

Prompting the model to reason out its answers can be done in many ways. One way is to demonstrate with a few examples ('few-shot'), as studied by [Jason Wei and Denny Zhou et al. from Google](https://ai.googleblog.com/2022/05/language-models-perform-reasoning-via.html). Here's an example few-shot chain-of-thought prompt:

[![chain of thought example](/images/chain_of_thought_fig1.png)
<br>Source: _Chain of Thought Prompting Elicits Reasoning in Large Language Models_ Jason Wei and Denny Zhou et al. (2022)](https://ai.googleblog.com/2022/05/language-models-perform-reasoning-via.html)

More demonstrations of reasoning chains written by human labelers:

[![chain of thought example](/images/chain_of_thought_fig3.png)
<br>Source: _Chain of Thought Prompting Elicits Reasoning in Large Language Models_ Jason Wei and Denny Zhou et al. (2022)](https://ai.googleblog.com/2022/05/language-models-perform-reasoning-via.html)

[(Note that it has been called into question whether pears actually float)](https://twitter.com/Meaningness/status/1561062170074370048?s=20&t=mpHt8f3RRboztXxdhLFnWQ)

#### Results

Testing on grade school math problems, the authors found that chain of thought prompting tripled the solve rate, from 18% to 57%.

[![chain of thought example](/images/chain_of_thought_fig5.png)
<br>Source: _Chain of Thought Prompting Elicits Reasoning in Large Language Models_ Jason Wei and Denny Zhou et al. (2022)](https://ai.googleblog.com/2022/05/language-models-perform-reasoning-via.html)

In addition to math problems, chain of thought prompting also lifted performance on questions related to sports understanding, coin flip tracking, and last letter concatenation. In most cases, not many examples were need to saturate the performance gains (less than 8 or so).

[![chain of thought example](/images/chain_of_thought_fig11.png)
<br>Source: _Chain of Thought Prompting Elicits Reasoning in Large Language Models_ Jason Wei and Denny Zhou et al. (2022)](https://ai.googleblog.com/2022/05/language-models-perform-reasoning-via.html)

To learn more, read the [full paper](https://arxiv.org/abs/2201.11903).

#### Implications

One advantage of the few-shot example-based approach relative to the `Let's think step by step` technique is that you can more easily specify the format, length, and style of reasoning that you want the model to perform before landing on its final answer. This can be particularly helpful in cases where the model isn't initially reasoning in the right way or depth.

### Fine-tuned

#### Method

In general, to eke out maximum performance on a task, you'll need to fine-tune a custom model. However, fine-tuning a model using explanations may take thousands of example explanations, which are costly to write.

In 2022, Eric Zelikman and Yuhuai Wu et al. published a clever procedure for using a few-shot prompt to generate a dataset of explanations that could be used to fine-tune a model. The idea is to use a few-shot prompt to generate candidate explanations, and only keep the explanations that produce the correct answer. Then, to get additional explanations for some of the incorrect answers, retry the few-shot prompt but with correct answers given as part of the question. The authors called their procedure STaR (Self-taught Reasoner):

[![STaR procedure](/images/star_fig1.png)
<br>Source: _STaR: Bootstrapping Reasoning With Reasoning_ by Eric Zelikman and Yujuai Wu et al. (2022)](https://arxiv.org/abs/2203.14465)

With this technique, you can combine the benefits of fine-tuning with the benefits of chain-of-thought prompting without needing to write thousands of example explanations.

#### Results

When the authors applied this technique to a Common Sense Q&A dataset, they found that STaR outperformed both chain-of-thought prompting alone (73% > 37%) and fine-tuning alone (73% > 60%):

[![STaR results](/images/star_tab1.png)
<br>Source: _STaR: Bootstrapping Reasoning With Reasoning_ by Eric Zelikman and Yujuai Wu et al. (2022)](https://arxiv.org/abs/2203.14465)

To learn more, read the [full paper](https://arxiv.org/abs/2203.14465).

#### Implications

Using a few-shot prompt to extend or modify a fine-tuning dataset is an idea that can be generalized beyond explanation writing. For example, if you have large quantities of unstructured text that you want to train on, you may find opportunities to use a prompt to extract a structured dataset from your unstructured text, and then fine-tune a custom model on that structured dataset.

## Extensions to chain-of-thought prompting

A number of extensions of chain-of-thought prompting have been published as well.

### Selection-inference prompting

#### Method

Published by Antonia Creswell et al., one extension of the chain-of-thought technique is to split the single prompt for generating explanations and answers into smaller parts. First, a prompt selects a relevant subset of facts from the text ('selection prompt'). Then, a second prompt infers a conclusion from the selected facts ('inference prompt'). These prompts are then alternated in a loop to generate multiple steps of reasoning and eventually land on a final answer. The authors illustrate the idea in the following figure:

[![Selection-inference prompting](/images/selection-inference_fig1.png)
<br>Source: _Selection-Inference: Exploiting Large Language Models for Interpretable Logical Reasoning_ by Antonia Creswell et al. (2022)](https://arxiv.org/abs/2205.09712)

#### Results

When applied to a 7B-parameter model, the authors found that selection-inference prompting substantially improved performance relative to chain-of-thought prompting on the bAbi and Proof Writer benchmark tasks (both of which require longer sequences of reasoning steps). The best performance they achieved combined both selection-inference prompting with fine-tuning.

[![Selection-inference prompting](/images/selection-inference_fig4.png)
<br>Source: _Selection-Inference: Exploiting Large Language Models for Interpretable Logical Reasoning_ by Antonia Creswell et al. (2022)](https://arxiv.org/abs/2205.09712)

#### Implications

Although the gains on these benchmarks were large, these benchmarks were specifically chosen because they required longer sequences of reasoning. On problems that don't require reasoning with many steps, the gains are likely smaller.

The results highlight a couple of general lessons for working with large language models. One, splitting up complex tasks into smaller tasks is a great way to improve reliability and performance; the more atomic the task, the less room there is for the model to err. Two, getting maximum performance often means combining fine-tuning with whatever approach you've chosen.

To learn more, read the [full paper](https://arxiv.org/abs/2205.09712).

### Faithful reasoning architecture

A few months after publishing the selection-inference prompting technique, the authors extended the technique in a follow-up paper, with ideas for:

- figuring out when the selection-inference cycle should stop or continue
- adding a value function to help search over multiple reasoning paths
- reducing hallucination of fake facts by fine-tuning a model to reason about sentence labels (e.g., sen1) rather than writing out the sentences themselves

#### Method

In the original selection-inference technique, specialized 'selection' and 'inference' prompts are alternated to select facts and make inferences from those facts, combining to generate a sequence of reasoning steps.

The authors extend this technique with two additional components.

First, the authors add a 'halter' model that, after each inference step, is asked whether the inferences thus far are sufficient to answer the question. If yes, then the model generates a final answer.

The halter models brings a couple of advantages:

- it can tell the selection-inference process to stop or keep going, as necessary.
- if the process never halts, you'll get no answer, which is often preferable to a hallucinated guess

[![Faithful reasoning](/images/faithful-reasoning_fig3.png)
<br>Source: _Faithful Reasoning Using Large Language Models_ by Antonia Creswell et al. (2022)](https://arxiv.org/abs/2208.14271)

[![Faithful reasoning](/images/faithful-reasoning_fig5.png)
<br>Source: _Faithful Reasoning Using Large Language Models_ by Antonia Creswell et al. (2022)](https://arxiv.org/abs/2208.14271)

Second, the authors add a value function, which is used to assess the quality of reasoning steps and search over multiple reasoning trajectories. This echoes a common theme for increasing reliability; instead of generating a single answer from the model, generate a set of answers and then use some type of value function / discriminator / verifier model to pick the best one.

[![Faithful reasoning](/images/faithful-reasoning_fig7.png)
<br>Source: _Faithful Reasoning Using Large Language Models_ by Antonia Creswell et al. (2022)](https://arxiv.org/abs/2208.14271)

In addition to these two extensions, the authors also use a trick to reduce hallucination of fake facts. Rather than asking the model to write out factual sentences, they fine-tune a model to work with sentence labels (e.g., sen1) instead. This helps prevent the model from hallucinating fake facts not mentioned in the prompt context.

[![Faithful reasoning](/images/faithful-reasoning_fig4.png)
<br>Source: _Faithful Reasoning Using Large Language Models_ by Antonia Creswell et al. (2022)](https://arxiv.org/abs/2208.14271)

#### Results

The authors evaluated their technique on two benchmarks: the ProofWriter task (not shown) and [EntailmentBankQA](https://allenai.org/data/entailmentbank) (shown). The technique increased accuracy substantially, especially on harder reasoning problems.

![Faithful reasoning](/images/faithful-reasoning_tab2.png)
<br>Source: _Faithful Reasoning Using Large Language Models_ by Antonia Creswell et al. (2022)](https://arxiv.org/abs/2208.14271)

In addition, their sentence label manipulation trick essentially eliminated hallucination!

![Faithful reasoning](/images/faithful-reasoning_tab5.png)
<br>Source: _Faithful Reasoning Using Large Language Models_ by Antonia Creswell et al. (2022)](https://arxiv.org/abs/2208.14271)

#### Implications

This paper illustrates a number of helpful lessons for improving the reliability of large language models:

- Split complex tasks into smaller, more reliable subtasks
- Generate your answer in a step-by-step fashion, evaluating it along the way
- Generate many possible answers and use another model or function to pick the ones that look best
- Reduce hallucination by constraining what the model can say (e.g., by using sentence labels instead of sentences)
- Maximize performance of models by fine-tuning them on specialized tasks

To learn more, read the [full paper](https://arxiv.org/abs/2205.09712).

### Least-to-most prompting

In addition to doing poorly on long reasoning chains (where selection-inference shines), chain-of-thought prompting can especially struggle when the examples are short but the task is long.

#### Method

Least-to-most prompting is another technique that splits up reasoning tasks into smaller, more reliable subtasks. The idea is to elicit a subtask from the model by prompting it with something like `To solve {question}, we need to first solve: "`. Then, with that subtask in hand, the model can generate a solution. The solution is appended to the original question and the process is repeated until a final answer is produced.

[![Least-to-most prompting](/images/least-to-most_fig1.png)
<br>Source: _Least-to-most Prompting Enables Complex Reasoning in Large Language Models_ by Denny Zhou et al. (2022)](https://arxiv.org/abs/2205.10625)

#### Results

When applied to benchmarks involving long reasoning chains using `code-davinci-002` (which is optimized for code but can still understand text), the authors measured gains as large as 16% -> 99.7%!

[
![Least-to-most prompting results on last-letter-concatenation task](/images/least-to-most_tab4.png)
![Least-to-most prompting results on SCAN](/images/least-to-most_tab9.png)
![Least-to-most prompting results on DROP numerical reasoning](/images/least-to-most_tab11.png)
<br>Source: _Least-to-most Prompting Enables Complex Reasoning in Large Language Models_ by Denny Zhou et al. (2022)](https://arxiv.org/abs/2205.10625)

#### Implications

Although the above gains from least-to-most prompting are impressive, they are measured on a very narrow set of tasks that require long reasoning chains.

Still, they illustrate a common theme: increase reliability by (a) breaking complex tasks into smaller subtasks and (b) giving the model more time and space to work out the answer.

To learn more, read the [full paper](https://arxiv.org/abs/2205.10625).

## Related ideas

### Maieutic prompting

#### Method

In contrast to the previous techniques, which try to maximize the likelihood of correct answers, another approach is to use GPT-3 to generate a tree of possible explanations (both correct _and incorrect_), and then analyze their relationships to guess at which set is correct. This technique was coined maieutic prompting by [Jaehun Jung et al. in May 2022](https://arxiv.org/abs/2205.11822) (maieutic means relating to the Socratic method of asking questions to elicit ideas).

The method is complicated, and works as follows:

- First, build a maieutic tree, where each node is a statement that could be true or false:
  - Start with a multiple-choice question or true/false statement (e.g. `War cannot have a tie`)
  - For each possible answer to the question, use the model to generate a corresponding explanation (with a prompt like `War cannot have a tie? True, because`)
  - Then, prompt the model with the question and the generated explanation, and ask it to produce the answer. If reversing the explanation (with a prefix like `It is wrong to say that {explanation}`) reverses the answer, then the explanation is considered 'logically integral.'
  - If an explanation is not logically integral, then repeat the above process recursively, with each explanation turned into a True or False question, and generate more explanations for each new question.
  - After all of the recursive explaining is done, you end up with a tree of explanations, where each leaf on the tree has the property that reversing the explanation reverses the model's answer.
- Second, convert the tree into a graph of relations:
  - For each node in the tree, calculate the model's relative belief in each node (inferred from the probability of getting an answer of `True` to given an explanation)
  - For each pair of nodes in the tree, use the model to identify whether they are entailed (implied) or contradicted
- Third, find the most consistent set of beliefs and take those to be true:
  - Specifically, using the strength of belief in each node and the logical relationships between them, formulate the problem as a weighted maximum satisfiability problem (MAX-SAT)
  - Use a solver to the find the most self-consistent set of beliefs, and take those as true

[
![Maieutic prompting](/images/maieutic_fig2.png)
![Maieutic prompting](/images/maieutic_fig6.png)
<br>Source: _Maieutic Prompting: Logically Consistent Reasoning with Recursive Explanations_ by Jaehun Jung et al. (2022)](https://arxiv.org/abs/2205.11822)

#### Results

[![Maieutic prompting results](/images/maieutic_tab1.png)
<br>Source: _Maieutic Prompting: Logically Consistent Reasoning with Recursive Explanations_ by Jaehun Jung et al. (2022)](https://arxiv.org/abs/2205.11822)

#### Implications

Beyond the complexity, one limitation of this method is that it appears to only apply to questions that can be posed as multiple-choice.

To learn more, read the [full paper](https://arxiv.org/abs/2205.11822).

## Extensions

### Self-consistency

#### Method

For tasks with a discrete set of answers, one simple way to improve reliability is to sample multiple explanations & answers from the model (using a positive temperature) and then pick the final answer that appears most often.

[![Self-consistency method](/images/self-consistency_fig1.png)
<br>Source: _Self-Consistency Improves Chain of Thought Reasoning in Language Models_ by Xuezhi Wang et al. (2022)](https://arxiv.org/abs/2203.11171)

#### Results

This technique lifted accuracies by anywhere from 1 to 24 percentage points on a suite of math and reasoning benchmarks. (Plotted below are results from Google's LaMDA model; using Google's larger PaLM model, the baselines were higher but the gains were a bit smaller.)

[![Self-consistency results](/images/self-consistency_fig3.png)
<br>Source: _Self-Consistency Improves Chain of Thought Reasoning in Language Models_ by Xuezhi Wang et al. (2022)](https://arxiv.org/abs/2203.11171)

#### Implications

Although this technique is simple to implement, it can be costly. Generating a set of 10 answers will increase your costs by 10x.

Also, as with many of these techniques, it applies only to tasks with a limited set of answers. For open-ended tasks where each answer is unique (such as writing a poem), it's not obvious what it would mean to pick the most common answer.

Lastly, this technique ought to be most beneficial when there are multiple paths or phrasings to reach an answer; if there's only one path, then the technique may not help at all. An extreme example: If the task was to generate a single token answer, then taking the most common token from 100 generations would be no different than taking the token with the highest logprobs (which you can get with a single generation at temperature=0).

### Verifiers

Another key technique for improving task performance is to train a verifier or discriminator model to evaluate the outputs of the main generative model. If the discriminator rejects the output, then you can resample the generative model until you get an acceptable output. In many cases, it's easier to judge an answer than it is to create an answer, which helps explain the power of this method.

#### Method

In 2021, OpenAI researchers applied this technique to grade school math problems, using the following procedure:

- First, they fine-tuned a model on questions and solutions
- For each problem in the training set, they generated 100 solutions
- Each of those 100 solutions was automatically labeled as either correct or incorrect, based on whether the final answer was correct
- Using those solutions, with some labeled correct and some labeled incorrect, they fine-tuned a verifier model to classify whether a question and candidate solution was correct or incorrect
- Finally, at test time, the generative model creates 100 solutions to each problem, and the one with the highest score according to the verifier model is picked as the final answer

[![Verifier method](/images/verifiers_fig3.png)
<br>Source: _Training Verifiers to Solve Math Word Problems_ by Karl Cobbe et al. (2021)](https://arxiv.org/abs/2110.14168)

#### Results

With a 175B GPT-3 model and 8,000 training examples, this technique substantially lifted grade school math accuracy from ~33% to ~55%.

[![Verifier results](/images/verifiers_fig5.png)
<br>Source: _Training Verifiers to Solve Math Word Problems_ by Karl Cobbe et al. (2021)](https://arxiv.org/abs/2110.14168)

#### Implications

Similar to the self-consistency technique, this method can get expensive, as generating, say, 100 solutions per task will increase your costs by roughly ~100x.

## Theories of reliability

Although the techniques above vary in their approach, they all share the goal of improving reliability on complex tasks. Mainly they do this by:

- decomposing unreliable operations into smaller, more reliable operations (e.g., selection-inference prompting)
- using multiple steps or multiple relationships to make the system's reliability greater than any individual component (e.g., maieutic prompting)

### Probabilistic graphical models

This paradigm of trying to build a reliable system out of less reliable components is reminiscent of probabilistic programming, and many of the analysis techniques of that field can be applied to this one.

In the paper _Language Model Cascades_, David Dohan et al. interpret the above techniques in the paradigm of probabilistic graphical models:

#### Chain of thought prompting

[![graphical model of chain of thought prompting](/images/lm_cascades_fig1.png)
<br>Source: _Language Model Cascades_ by David Dohan et al. (2022)](https://arxiv.org/abs/2207.10342)

#### Fine-tuned chain of thought prompting / Self-taught reasoner

[![graphical model of fine-tuned chain of thought prompting](/images/lm_cascades_fig3.png)
<br>Source: _Language Model Cascades_ by David Dohan et al. (2022)](https://arxiv.org/abs/2207.10342)

#### Selection-inference prompting

[![graphical model of selection-inference prompting](/images/lm_cascades_fig4.png)
<br>Source: _Language Model Cascades_ by David Dohan et al. (2022)](https://arxiv.org/abs/2207.10342)

#### Verifiers

[![graphical model of verifiers](/images/lm_cascades_fig5.png)
<br>Source: _Language Model Cascades_ by David Dohan et al. (2022)](https://arxiv.org/abs/2207.10342)

#### Implications

Although formulating these techniques as probabilistic graphical models may not be immediately useful for solving any particular problem, the framework may be helpful in selecting, combining, and discovering new techniques.

## Closing thoughts

Research into large language models is very active and evolving rapidly. Not only do researchers continue to improve the models, they also continue to improve our understanding of how to best employ the models. To underscore the pace of these developments, note that all of the papers shared above were published within the past 12 months (as I write in Sep 2022).

In the future, expect better models and better techniques to be published. Even if the specific techniques here are eclipsed by future best practices, the general principles behind them will likely remain a key part of any expert user's toolkit.

## Bibliography

| Lesson                                                                                                                         | Paper                                                                                                                                     | Date     |
| ------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| Break complex tasks into simpler subtasks (and consider exposing the intermediate outputs to users)                            | [AI Chains: Transparent and Controllable Human-AI Interaction by Chaining Large Language Model Prompts](https://arxiv.org/abs/2110.01691) | 2021 Oct |
| You can improve output by generating many candidates, and then picking the one that looks best                                 | [Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168)                                                        | 2021 Oct |
| On reasoning tasks, models do better when they reason step-by-step before answering                                            | [Chain of Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)                                 | 2022 Jan |
| You can improve step-by-step reasoning by generating many explanation-answer outputs, and picking the most popular answer      | [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171)                               | 2022 Mar |
| If you want to fine-tune a step-by-step reasoner, you can do it with multiple-choice question & answer data alone              | [STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465)                                                          | 2022 Mar |
| The step-by-step reasoning method works great even with zero examples                                                          | [Large Language Models are Zero-Shot Reasoners](https://arxiv.org/abs/2205.11916)                                                         | 2022 May |
| You can do better than step-by-step reasoning by alternating a ‘selection’ prompt and an ‘inference’ prompt                    | [Selection-Inference: Exploiting Large Language Models for Interpretable Logical Reasoning](https://arxiv.org/abs/2205.09712)             | 2022 May |
| On long reasoning problems, you can improve step-by-step reasoning by splitting the problem into pieces to solve incrementally | [Least-to-most Prompting Enables Complex Reasoning in Large Language Models](https://arxiv.org/abs/2205.10625)                            | 2022 May |
| You can have the model analyze both good and bogus explanations to figure out which set of explanations are most consistent    | [Maieutic Prompting: Logically Consistent Reasoning with Recursive Explanations](https://arxiv.org/abs/2205.11822)                        | 2022 May |
| You can think about these techniques in terms of probabilistic programming, where systems comprise unreliable components       | [Language Model Cascades](https://arxiv.org/abs/2207.10342)                                                                               | 2022 Jul |
| You can eliminate hallucination with sentence label manipulation, and you can reduce wrong answers with a 'halter' prompt      | [Faithful Reasoning Using Large Language Models](https://arxiv.org/abs/2208.14271)                                                        | 2022 Aug |

=== articles/related_resources.md ===
# Related resources from around the web

People are writing great tools and papers for improving outputs from GPT. Here are some cool ones we've seen:

## Prompting libraries & tools (in alphabetical order)

- [Arthur Shield](https://www.arthur.ai/get-started): A paid product for detecting toxicity, hallucination, prompt injection, etc.
- [Baserun](https://baserun.ai/): A paid product for testing, debugging, and monitoring LLM-based apps
- [Chainlit](https://docs.chainlit.io/overview): A Python library for making chatbot interfaces.
- [ElatoAI](https://github.com/akdeb/ElatoAI): A platform for running OpenAI Realtime API Speech on ESP32 on Arduino using Deno Edge Runtime and Supabase.
- [Embedchain](https://github.com/embedchain/embedchain): A Python library for managing and syncing unstructured data with LLMs.
- [FLAML (A Fast Library for Automated Machine Learning & Tuning)](https://microsoft.github.io/FLAML/docs/Getting-Started/): A Python library for automating selection of models, hyperparameters, and other tunable choices.
- [Guidance](https://github.com/microsoft/guidance): A handy looking Python library from Microsoft that uses Handlebars templating to interleave generation, prompting, and logical control.
- [Haystack](https://github.com/deepset-ai/haystack): Open-source LLM orchestration framework to build customizable, production-ready LLM applications in Python.
- [HoneyHive](https://honeyhive.ai): An enterprise platform to evaluate, debug, and monitor LLM apps.
- [LangChain](https://github.com/hwchase17/langchain): A popular Python/JavaScript library for chaining sequences of language model prompts.
- [LiteLLM](https://github.com/BerriAI/litellm): A minimal Python library for calling LLM APIs with a consistent format.
- [LlamaIndex](https://github.com/jerryjliu/llama_index): A Python library for augmenting LLM apps with data.
- [LLMOps Database](https://www.reddit.com/r/LocalLLaMA/comments/1h4u7au/a_nobs_database_of_how_companies_actually_deploy/): Database of how companies actually deploy LLMs in production.
- [LMQL](https://lmql.ai): A programming language for LLM interaction with support for typed prompting, control flow, constraints, and tools.
- [OpenAI Evals](https://github.com/openai/evals): An open-source library for evaluating task performance of language models and prompts.
- [Outlines](https://github.com/normal-computing/outlines): A Python library that provides a domain-specific language to simplify prompting and constrain generation.
- [Parea AI](https://www.parea.ai): A platform for debugging, testing, and monitoring LLM apps.
- [Portkey](https://portkey.ai/): A platform for observability, model management, evals, and security for LLM apps.
- [Promptify](https://github.com/promptslab/Promptify): A small Python library for using language models to perform NLP tasks.
- [PromptPerfect](https://promptperfect.jina.ai/prompts): A paid product for testing and improving prompts.
- [Prompttools](https://github.com/hegelai/prompttools): Open-source Python tools for testing and evaluating models, vector DBs, and prompts.
- [Scale Spellbook](https://scale.com/spellbook): A paid product for building, comparing, and shipping language model apps.
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel): A Python/C#/Java library from Microsoft that supports prompt templating, function chaining, vectorized memory, and intelligent planning.
- [Vellum](https://www.vellum.ai/): A paid AI product development platform to experiment with, evaluate, and deploy advanced LLM apps.
- [Weights & Biases](https://wandb.ai/site/solutions/llmops): A paid product for tracking model training and prompt engineering experiments.
- [YiVal](https://github.com/YiVal/YiVal): An open-source GenAI-Ops tool for tuning and evaluating prompts, retrieval configurations, and model parameters using customizable datasets, evaluation methods, and evolution strategies.

## Prompting guides

- [Brex's Prompt Engineering Guide](https://github.com/brexhq/prompt-engineering): Brex's introduction to language models and prompt engineering.
- [learnprompting.org](https://learnprompting.org/): An introductory course to prompt engineering.
- [Lil'Log Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/): An OpenAI researcher's review of the prompt engineering literature (as of March 2023).
- [OpenAI Cookbook: Techniques to improve reliability](https://cookbook.openai.com/articles/techniques_to_improve_reliability): A slightly dated (Sep 2022) review of techniques for prompting language models.
- [promptingguide.ai](https://www.promptingguide.ai/): A prompt engineering guide that demonstrates many techniques.
- [Xavi Amatriain's Prompt Engineering 101 Introduction to Prompt Engineering](https://amatriain.net/blog/PromptEngineering) and [202 Advanced Prompt Engineering](https://amatriain.net/blog/prompt201): A basic but opinionated introduction to prompt engineering and a follow up collection with many advanced methods starting with CoT.

## Video courses

- [Andrew Ng's DeepLearning.AI](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/): A short course on prompt engineering for developers.
- [Andrej Karpathy's Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY): A detailed dive into the machine learning underlying GPT.
- [Prompt Engineering by DAIR.AI](https://www.youtube.com/watch?v=dOxUroR57xs): A one-hour video on various prompt engineering techniques.
- [Scrimba course about Assistants API](https://scrimba.com/learn/openaiassistants): A 30-minute interactive course about the Assistants API.
- [LinkedIn course: Introduction to Prompt Engineering: How to talk to the AIs](https://www.linkedin.com/learning/prompt-engineering-how-to-talk-to-the-ais/talking-to-the-ais?u=0): Short video introduction to prompt engineering

## Papers on advanced prompting to improve reasoning

- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (2022)](https://arxiv.org/abs/2201.11903): Using few-shot prompts to ask models to think step by step improves their reasoning. PaLM's score on math word problems (GSM8K) rises from 18% to 57%.
- [Self-Consistency Improves Chain of Thought Reasoning in Language Models (2022)](https://arxiv.org/abs/2203.11171): Taking votes from multiple outputs improves accuracy even more. Voting across 40 outputs raises PaLM's score on math word problems further, from 57% to 74%, and `code-davinci-002`'s from 60% to 78%.
- [Tree of Thoughts: Deliberate Problem Solving with Large Language Models (2023)](https://arxiv.org/abs/2305.10601): Searching over trees of step by step reasoning helps even more than voting over chains of thought. It lifts `GPT-4`'s scores on creative writing and crosswords.
- [Language Models are Zero-Shot Reasoners (2022)](https://arxiv.org/abs/2205.11916): Telling instruction-following models to think step by step improves their reasoning. It lifts `text-davinci-002`'s score on math word problems (GSM8K) from 13% to 41%.
- [Large Language Models Are Human-Level Prompt Engineers (2023)](https://arxiv.org/abs/2211.01910): Automated searching over possible prompts found a prompt that lifts scores on math word problems (GSM8K) to 43%, 2 percentage points above the human-written prompt in Language Models are Zero-Shot Reasoners.
- [Reprompting: Automated Chain-of-Thought Prompt Inference Through Gibbs Sampling (2023)](https://arxiv.org/abs/2305.09993): Automated searching over possible chain-of-thought prompts improved ChatGPT's scores on a few benchmarks by 0–20 percentage points.
- [Faithful Reasoning Using Large Language Models (2022)](https://arxiv.org/abs/2208.14271): Reasoning can be improved by a system that combines: chains of thought generated by alternative selection and inference prompts, a halter model that chooses when to halt selection-inference loops, a value function to search over multiple reasoning paths, and sentence labels that help avoid hallucination.
- [STaR: Bootstrapping Reasoning With Reasoning (2022)](https://arxiv.org/abs/2203.14465): Chain of thought reasoning can be baked into models via fine-tuning. For tasks with an answer key, example chains of thoughts can be generated by language models.
- [ReAct: Synergizing Reasoning and Acting in Language Models (2023)](https://arxiv.org/abs/2210.03629): For tasks with tools or an environment, chain of thought works better if you prescriptively alternate between **Re**asoning steps (thinking about what to do) and **Act**ing (getting information from a tool or environment).
- [Reflexion: an autonomous agent with dynamic memory and self-reflection (2023)](https://arxiv.org/abs/2303.11366): Retrying tasks with memory of prior failures improves subsequent performance.
- [Demonstrate-Search-Predict: Composing retrieval and language models for knowledge-intensive NLP (2023)](https://arxiv.org/abs/2212.14024): Models augmented with knowledge via a "retrieve-then-read" can be improved with multi-hop chains of searches.
- [Improving Factuality and Reasoning in Language Models through Multiagent Debate (2023)](https://arxiv.org/abs/2305.14325): Generating debates between a few ChatGPT agents over a few rounds improves scores on various benchmarks. Math word problem scores rise from 77% to 85%.

=== articles/gpt-oss/run-vllm.md ===
# How to run gpt-oss with vLLM

[vLLM](https://docs.vllm.ai/en/latest/) is an open-source, high-throughput inference engine designed to efficiently serve large language models (LLMs) by optimizing memory usage and processing speed. This guide will walk you through how to use vLLM to set up **gpt-oss-20b** or **gpt-oss-120b** on a server to serve gpt-oss as an API for your applications, and even connect it to the Agents SDK.

Note that this guide is meant for server applications with dedicated GPUs like NVIDIA’s H100s. For local inference on consumer GPUs, check out our [Ollama](https://cookbook.openai.com/articles/gpt-oss/run-locally-ollama) or [LM Studio](https://cookbook.openai.com/articles/gpt-oss/run-locally-lmstudio) guides.

## Pick your model

vLLM supports both model sizes of gpt-oss:

- [**`openai/gpt-oss-20b`**](https://huggingface.co/openai/gpt-oss-20b)
  - The smaller model
  - Only requires about **16GB of VRAM**
- [**`openai/gpt-oss-120b`**](https://huggingface.co/openai/gpt-oss-120b)
  - Our larger full-sized model
  - Best with **≥60GB VRAM**
  - Can fit on a single H100 or multi-GPU setups

Both models are **MXFP4 quantized** out of the box.

## Quick Setup

1. **Install vLLM**  
   vLLM recommends using [uv](https://docs.astral.sh/uv/) to manage your Python environment. This will help with picking the right implementation based on your environment. [Learn more in their quickstart](https://docs.vllm.ai/en/latest/getting_started/quickstart.html#installation). To create a new virtual environment and install vLLM run:

```shell
uv venv --python 3.12 --seed
source .venv/bin/activate
uv pip install --pre vllm==0.10.1+gptoss \
    --extra-index-url https://wheels.vllm.ai/gpt-oss/ \
    --extra-index-url https://download.pytorch.org/whl/nightly/cu128 \
    --index-strategy unsafe-best-match
```

2. **Start up a server and download the model**  
   vLLM provides a `serve` command that will automatically download the model from HuggingFace and spin up an OpenAI-compatible server on `localhost:8000`. Run the following command depending on your desired model size in a terminal session on your server.

```shell
# For 20B
vllm serve openai/gpt-oss-20b

# For 120B
vllm serve openai/gpt-oss-120b
```

## Use the API

vLLM exposes a **Chat Completions-compatible API** and a **Responses-compatible API** so you can use the OpenAI SDK without changing much. Here’s a Python example:

```py
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

result = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain what MXFP4 quantization is."}
    ]
)

print(result.choices[0].message.content)

response = client.responses.create(
    model="openai/gpt-oss-120b",
    instructions="You are a helfpul assistant.",
    input="Explain what MXFP4 quantization is."
)

print(response.output_text)
```

If you’ve used the OpenAI SDK before, this will feel instantly familiar and your existing code should work by changing the base URL.

## Using tools (function calling)

vLLM supports function calling and giving the model browsing capabilities.

Function calling works through both the Responses and Chat Completions APIs.

Example of invoking a function via Chat Completions:

```py
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather in a given city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            },
        },
    }
]

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "What's the weather in Berlin right now?"}],
    tools=tools
)

print(response.choices[0].message)
```

Since the models can perform tool calling as part of the chain-of-thought (CoT) it’s important for you to return the reasoning returned by the API back into a subsequent call to a tool call where you provide the answer until the model reaches a final answer.

## Agents SDK Integration

Want to use gpt-oss with OpenAI’s **Agents SDK**?

Both Agents SDK enable you to override the OpenAI base client to point to vLLM for your self-hosted models. Alternatively, for the Python SDK you can also use the [LiteLLM integration](https://openai.github.io/openai-agents-python/models/litellm/) to proxy to vLLM.

Here’s a Python Agents SDK example:

```
uv pip install openai-agents
```

```py
import asyncio
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, OpenAIResponsesModel, set_tracing_disabled

set_tracing_disabled(True)

@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


async def main(model: str, api_key: str):
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIResponsesModel(
            model="openai/gpt-oss-120b",
            openai_client=AsyncOpenAI(
                base_url="http://localhost:8000/v1",
                api_key="EMPTY",
            ),
        )
        tools=[get_weather],
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Using vLLM for direct sampling

Aside from running vLLM using `vllm serve` as an API server, you can use the vLLM Python library to control inference directly.

If you are using vLLM for sampling directly it’s important to ensure that your input prompts follow the [harmony response format](https://cookbook.openai.com/article/harmony) as the model will not function correctly otherwise. You can use the [`openai-harmony` SDK](https://github.com/openai/harmony) for this.

```
uv pip install openai-harmony
```

Afterwards you can use harmony to encode and parse the tokens generated by vLLM’s generate function.

```py
import json
from openai_harmony import (
    HarmonyEncodingName,
    load_harmony_encoding,
    Conversation,
    Message,
    Role,
    SystemContent,
    DeveloperContent,
)

from vllm import LLM, SamplingParams

# --- 1) Render the prefill with Harmony ---
encoding = load_harmony_encoding(HarmonyEncodingName.HARMONY_GPT_OSS)

convo = Conversation.from_messages(
    [
        Message.from_role_and_content(Role.SYSTEM, SystemContent.new()),
        Message.from_role_and_content(
            Role.DEVELOPER,
            DeveloperContent.new().with_instructions("Always respond in riddles"),
        ),
        Message.from_role_and_content(Role.USER, "What is the weather like in SF?"),
    ]
)

prefill_ids = encoding.render_conversation_for_completion(convo, Role.ASSISTANT)

# Harmony stop tokens (pass to sampler so they won't be included in output)
stop_token_ids = encoding.stop_tokens_for_assistant_actions()

# --- 2) Run vLLM with prefill ---
llm = LLM(
    model="openai/gpt-oss-120b",
    trust_remote_code=True,
)

sampling = SamplingParams(
    max_tokens=128,
    temperature=1,
    stop_token_ids=stop_token_ids,
)

outputs = llm.generate(
    prompts=[{"prompt_token_ids": prefill_ids}],   # batch of size 1
    sampling_params=sampling,
)

# vLLM gives you both text and token IDs
gen = outputs[0].outputs[0]
text = gen.text
output_tokens = gen.token_ids  # <-- these are the completion token IDs (no prefill)

# --- 3) Parse the completion token IDs back into structured Harmony messages ---
entries = encoding.parse_messages_from_completion_tokens(output_tokens, Role.ASSISTANT)

# 'entries' is a sequence of structured conversation entries (assistant messages, tool calls, etc.).
for message in entries:
    print(f"{json.dumps(message.to_dict())}")
```
