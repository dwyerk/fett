"""Engine to extract information from tweets."""
import spacy

nlp = spacy.load('en')


def extract_ents(doc):
    """Extract entities from the Spacy NLP document."""
    for ent in doc.ents:
        yield ent

if __name__ == '__main__':
    texts = [
        u"GM L'Enfant! The truck is back on 7th & Maryland Ave, NW (11-1:30)",
        u"The truck's on L between 19th & 20th (11-1:30)",
        u"The truck will be @NavyFederal 820 Follin Ln, Vienna, Va ⌚️11-2:00"
    ]
    for i, doc in enumerate(nlp.pipe(texts, batch_size=50, n_threads=4)):
        print("{}: {}".format(doc, doc.is_parsed))
        for ent in extract_ents(doc):
            print('-->', ent.label_, ent)
