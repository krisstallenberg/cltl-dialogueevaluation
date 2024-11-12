import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import os
from emissor.representation.scenario import Signal
from emissor.persistence import ScenarioStorage
from cltl.dialogue_evaluation.statistical_evaluation import StatisticalEvaluator
from emissor.representation.scenario import Modality
import cltl.dialogue_evaluation.utils.text_signal as text_signal_util


# Mock data for a conversation
data = {
    'Turn': [1, 2, 3, 4, 5, 6],
    'Speaker': ['A', 'B', 'A', 'B', 'A', 'B'],
    'Dialogue Act': ['Greeting', 'Question', 'Answer', 'Statement', 'Request', 'Confirmation'],
    'Emotion': ['Happy', 'Curious', 'Neutral', 'Satisfied', 'Hopeful', 'Affirmative']
}

def get_signal_anotation(signals:[Signal]):
    data = []
    for i, signal in enumerate(signals):
        speaker = text_signal_util.get_speaker_from_text_signal(signal)
        text = ''.join(signal.seq)
        score = 0
        score += text_signal_util.get_sentiment_score_from_text_signal(signal)
        score += text_signal_util.get_dact_feedback_score_from_text_signal(signal)
        label = make_label(signal)
        row = {'turn':i, 'utterance': text, 'score': score, "speaker": speaker, "type":signal.modality, "label": label}
        data.append(row)
    return data

def make_label (signal):
    label = ""
    dacts = text_signal_util.get_dact_from_text_signal(signal)
    gos = text_signal_util.get_go_from_text_signal(signal)
    ekmans = text_signal_util.get_ekman_from_text_signal(signal)
    sentiments = text_signal_util.get_sentiment_from_text_signal(signal)
    print("Before getting label")
    print(dacts)
    print(gos)
    print(ekmans)
    print(sentiments)
    if dacts:
        label += dacts[0][0]
    if sentiments:
        label += sentiments[0][0]
    if gos:
        label += gos[0][0]
    if ekmans:
        label += ekmans[0][0]
    # JSON(value='love', type='GO', confidence=0.890785276889801)
    # JSON(value='joy', type='EKMAN', confidence=0.9762245354068)
    # JSON(value='positive', type='SENTIMENT', confidence=0.9762245354068)
    # JSON(value='complaint', type='MIDAS', confidence=0.2305116355419159)
    return label


def create_timeline_image(scenario_path, scenario, signals:[Signal]):
   # earliest, latest, period, activity_in_period = get_activity_in_period(story_of_life, current_date=current_date)
    rows = get_signal_anotation(signals)
    df = pd.DataFrame(rows)
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    print(df.head())
 #   ax = sns.scatterplot(x='time', y='sentiment', hue='label', data=df, size="certainty", style='label', palette="deep", sizes=(20, 200), legend="full")
    ax = sns.lineplot(x='turn', y='score', hue = 'label', data=df, palette="deep", legend="full")

    for index, row in df.iterrows():
        x = row['turn']
        y = row['score']
        category = row['speaker']+"\n"+str(row['utterance'])
        category += '\n'+str(row['label'])
        #category + str(row['ekman'])
        # actors = row['actors']
        # polarity = row['polarity']
        # emotion = row['emotion']

        ax.text(x, y,
                s=" " + str(category),
                rotation=70,
                horizontalalignment='left', size='small', color='black', verticalalignment='bottom',
                linespacing=1)

    ax.tick_params(axis='x', rotation=70)
    # Show the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    path =  os.path.join(scenario_path, scenario+"_plot.png")
    # plt.savefig(path, dpi=300, transparent=True)
    plt.savefig(path)
    plt.show()



def main():
    emissor_path = '/Users/piek/Desktop/d-Leolani/tutorials/test22/cltl-text-to-ekg-app/app/py-app/storage/emissor'
    emissor_path ="/Users/piek/Desktop/t-MA-Combots-2024/code/ma-communicative-robots/leolani_text_to_ekg/storage/emissor"
    #emissor_path ="/Users/piek/Desktop/t-MA-Combots-2024/code/ma-communicative-robots/emissor_chat/emissor"
    #scenario = "9e589730-4485-4412-b8b1-701eecf87607"
    #scenario = "42c97d7d-80ff-4e81-9cae-a3702b6d5380"
    scenario = "8e2af227-f264-46ca-92f6-03d0838763ad"
    #scenario = "54807868-2d29-4def-82b3-78d6457b56a6"
    scenario ="6bc62457-8889-4e34-951a-cec3193a39e0"
    scenario_path = os.path.join(emissor_path, scenario)
    print(scenario_path)
    scenario_storage = ScenarioStorage(emissor_path)
    scenario_ctrl = scenario_storage.load_scenario(scenario)
    text_signals = scenario_ctrl.get_signals(Modality.TEXT)
    create_timeline_image(scenario_path=scenario_path, scenario=scenario, signals=text_signals)
    # image_signals = scenario_ctrl.get_signals(Modality.IMAGE)
    #
    # evaluator = StatisticalEvaluator()
    # annotations = evaluator._get_annotation_dict(emissor_path, scenario)

if __name__ == '__main__':
    main()
