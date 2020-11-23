import chains
import json
from pprint import pprint
import itertools
import tqdm
import sys
from os import path

verbose = False
validation = False

def story_answer(story):
    """Tells you the correct answer. Return (storyid, index). 1 for the first ending, 2 for the second ending"""
    #obviously you can't use this information until you've chosen your answer!
    return story.InputStoryid, story.AnswerRightEnding

def parse_test_instance(story):
    """Returns TWO ParsedStory instances representing option 1 and 2"""
    # this is very compressed
    id = story.InputStoryid
    story = list(story)
    sentences = [chains.nlp(sentence) for sentence in story[2:6]]
    alternatives = [story[6], story[7]]
    return [chains.ParsedStory(id, id, chains.nlp(" ".join(story[2:6]+[a])), *(sentences+[chains.nlp(a)])) for a in alternatives]


if __name__ == "__main__":
    if "--build" in sys.argv:
        # load training data and build the model
        data, table = chains.process_corpus("train.csv")
        table.write("all.json")
        print("Successfully built the model")
        sys.exit(0)
    else:
        if not path.exists("all.json"):
            print("Load the model first using --load")

    # load the pre-built model
    with open("all.json") as fp:
        table = chains.ProbabilityTable(json.load(fp))

    total, correct = 0, 0

    # load testing data
    test = chains.load_data("test.csv")

    with open("answers.txt", "w") as f:
        # header for the csv
        f.write("InputStoryid,AnswerRightEnding\n")

        test_tqdm = tqdm.tqdm(test)
        for t in test_tqdm:
            one, two = parse_test_instance(t)

            _, one_deps = chains.extract_dependency_pairs(one)
            _, two_deps = chains.extract_dependency_pairs(two)

            # logic to choose between one and two
            prog_one = chains.protagonist(one)
            prog_two = chains.protagonist(two)

            pmi_one, pmi_two = 0, 0
            
            for entity_id, deps in one_deps.items():
                for first, second in list(zip(deps, deps[1:])):
                    pmi_one += table.pmi(first[0], first[1], second[0], second[1])

            for entity_id, deps in two_deps.items():
                for first, second in list(zip(deps, deps[1:])):
                    pmi_two += table.pmi(first[0], first[1], second[0], second[1])

            answer = "1" if pmi_one > pmi_two else "2"

            # write the predicted answer
            f.write(str(t.InputStoryid) + "," + answer + "\n")

            if validation:
                total += 1
                if answer == str(t.AnswerRightEnding):
                    correct += 1

                # print(answer + " " + str(t.AnswerRightEnding))

            # if total == 100:
            #     break

    if validation:
        print("Total: " + str(total))
        print("Correct: " + str(correct))
        print("Percentage: " + str((correct/total) * 100))
