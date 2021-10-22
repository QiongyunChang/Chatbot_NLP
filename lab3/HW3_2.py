
from spacy import displacy
import spacy
from spacy.training import Example
import random
from spacy.util import minibatch, compounding
from pathlib import Path
import  os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
TRAIN_DATA = [
              ("成功大學是一所酷學校", {"entities": [(0, 4, "ORG")]}),
              ("我在成功大學上課", {"entities": [(2, 6, "ORG")]}),
              ("成功大學受到豪雨的攻擊", {"entities": [(0, 4, "ORG")]}),
              ("他去年成功考進了成功大學", {"entities": [(8, 12, "ORG")]}),
              ("成功大學長久以來培育了各行各業無數的菁英領袖", {"entities": [(0, 4, "ORG")]}),
              ("成功大學特聘教授榮獲終生成就獎", {"entities": [(0, 4, "ORG")]}),
              ("成功大學副校長在去年退休", {"entities": [(0, 4, "ORG")]}),
              ]
text = \
"110年全國大專校院運動會復辦為期5天6項賽事圓滿落幕，\
今日下午在國立成功大學光復田徑場舉行熄聖火與交旗儀式。\
教育部體育署副署長洪志昌、國立成功大學校長蘇慧貞，以及下一屆承\
辦全大運國立體育大學校長邱炳坤皆出席與會。"
nlp = spacy.load('zh_core_web_lg')
doc = nlp(text)

doc = nlp(text)
for sent in doc.sents:
    print(">", sent)

for entity in doc.ents:
    print(entity, " ... ", entity.label_)

html = displacy.render(doc, style="ent")
output_path = Path("dependency_plot.html") #視覺化檔案儲存的檔名
output_path.open("w", encoding="utf-8").write(html)

pipe_exceptions = ["ner"] #指定我們只更新NER模型，其他的pipeline不去做變動
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# TRAINING THE MODEL
with nlp.disable_pipes(unaffected_pipes):

  # Training for 30 iterations
  for iteration in range(30):

    # shuufling examples  before every iteration
    random.shuffle(TRAIN_DATA)
    losses = {}
    # batch up the examples using spaCy's minibatch
    batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        texts, annotations = zip(*batch)

    example = []
    # Update the model with iterating each text
    for i in range(len(texts)):
        doc = nlp.make_doc(texts[i])
    example.append(Example.from_dict(doc, annotations[i]))

    # Update the model
    nlp.update(example, drop=0.5, losses=losses)
    print("Losses", losses)


doc = nlp(text)
print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
nlp.to_disk("./ncku_model")
