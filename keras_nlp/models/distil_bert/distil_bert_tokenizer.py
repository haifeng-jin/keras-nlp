# Copyright 2023 The KerasNLP Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""DistilBERT tokenizer."""

import copy

from keras_nlp.api_export import keras_nlp_export
from keras_nlp.models.distil_bert.distil_bert_presets import backbone_presets
from keras_nlp.tokenizers.word_piece_tokenizer import WordPieceTokenizer
from keras_nlp.utils.python_utils import classproperty


@keras_nlp_export("keras_nlp.models.DistilBertTokenizer")
class DistilBertTokenizer(WordPieceTokenizer):
    """A DistilBERT tokenizer using WordPiece subword segmentation.

    This tokenizer class will tokenize raw strings into integer sequences and
    is based on `keras_nlp.tokenizers.WordPieceTokenizer`. Unlike the
    underlying tokenizer, it will check for all special tokens needed by DistilBERT
    models and provides a `from_preset()` method to automatically download
    a matching vocabulary for a DistilBERT preset.

    This tokenizer does not provide truncation or padding of inputs. It can be
    combined with a `keras_nlp.models.DistilBertPreprocessor` layer for input packing.

    If input is a batch of strings (rank > 0), the layer will output a
    `tf.RaggedTensor` where the last dimension of the output is ragged.

    If input is a scalar string (rank == 0), the layer will output a dense
    `tf.Tensor` with static shape `[None]`.

    Args:
        vocabulary: A list of strings or a string filename path. If
            passing a list, each element of the list should be a single word
            piece token string. If passing a filename, the file should be a
            plain text file containing a single word piece token per line.
        lowercase: If true, the input text will be first lowered before
            tokenization.

    Examples:

    ```python
    # Unbatched input.
    tokenizer = keras_nlp.models.DistilBertTokenizer.from_preset(
        "distil_bert_base_en_uncased",
    )
    tokenizer("The quick brown fox jumped.")
    # Batched input.
    tokenizer(["The quick brown fox jumped.", "The fox slept."])
    # Detokenization.
    tokenizer.detokenize(tokenizer("The quick brown fox jumped."))
    # Custom vocabulary.
    vocab = ["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"]
    vocab += ["The", "quick", "brown", "fox", "jumped", "."]
    tokenizer = keras_nlp.models.DistilBertTokenizer(vocabulary=vocab)
    tokenizer("The quick brown fox jumped.")
    ```
    """

    def __init__(
        self,
        vocabulary,
        lowercase=False,
        **kwargs,
    ):
        super().__init__(
            vocabulary=vocabulary,
            lowercase=lowercase,
            **kwargs,
        )

        # Check for necessary special tokens.
        cls_token = "[CLS]"
        sep_token = "[SEP]"
        pad_token = "[PAD]"
        mask_token = "[MASK]"
        for token in [cls_token, pad_token, sep_token, mask_token]:
            if token not in self.get_vocabulary():
                raise ValueError(
                    f"Cannot find token `'{token}'` in the provided "
                    f"`vocabulary`. Please provide `'{token}'` in your "
                    "`vocabulary` or use a pretrained `vocabulary` name."
                )

        self.cls_token_id = self.token_to_id(cls_token)
        self.sep_token_id = self.token_to_id(sep_token)
        self.pad_token_id = self.token_to_id(pad_token)
        self.mask_token_id = self.token_to_id(mask_token)

    @classproperty
    def presets(cls):
        return copy.deepcopy(backbone_presets)
