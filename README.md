# ndc-aligned
Word-aligned Norwegian Dialect Corpus

## Data

The phonetic and orthographic transcriptions are available at (http://www.tekstlab.uio.no/scandiasyn/download.html). Unfortunately, the two transcription layers are not well aligned in the provided files:
- The number of utterances is not identical.
- The orthographic transcriptions contains quotation marks, whereas the phonetic transcriptions do not.
- In some files, the orthographic transcriptions of the last 1-2 utterances are missing.

The aligned data is provided in vertical format with some light-weight XML structure. Each utterance is embedded in a `<u>` tag with a running id number and the speaker identifier. Each token is given on one line, with the phonetic transcription first and the orthographic transcription second.

```
<doc id="aal_01um-02uk">
<u id="1" speaker="aal_01um">
ja	ja
ja	ja
</u>
...
</doc>
```

The aligned data is provided in the `aligned` folder.

## Process

The alignment process simply aligns one phonetic token with one orthographic token, skipping quotation marks. If the phonetic file is longer than the orthographic one, the last phonetic tokens are associated with the empty orthographic string, and these utterances are marked with the `missing_norm="yes"` attribute.

The script provides some additional checking procedures to make sure that the alignment is correct.

The script assumes tht the phonetic and orthographic transcriptions are in the `ndc_phon_with_informant_codes` and `ndc_with_informant_codes` folders respectively.
