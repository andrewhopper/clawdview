"""
Tests for embedding providers.
"""

import pytest
from unittest.mock import patch, MagicMock
import json


class TestBedrockEmbeddings:
    """Tests for AWS Bedrock embeddings."""

    def test_titan_embed_text(self, mock_boto3_session):
        """Test embedding single text with Titan."""
        from vectorstore_unified.embeddings import BedrockEmbeddings

        embeddings = BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v2:0",
            region="us-east-1",
        )

        result = embeddings.embed_text("Hello world")

        assert isinstance(result, list)
        assert len(result) == 1024
        assert all(isinstance(x, float) for x in result)

    def test_titan_embed_texts(self, mock_boto3_session):
        """Test embedding multiple texts with Titan."""
        from vectorstore_unified.embeddings import BedrockEmbeddings

        embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")

        texts = ["Hello", "World", "Test"]
        results = embeddings.embed_texts(texts)

        assert len(results) == 3
        assert all(len(emb) == 1024 for emb in results)

    def test_cohere_embed_text(self, mock_boto3_session):
        """Test embedding with Cohere model."""
        from vectorstore_unified.embeddings import BedrockEmbeddings

        embeddings = BedrockEmbeddings(model_id="cohere.embed-english-v3")

        result = embeddings.embed_text("Test text")

        assert isinstance(result, list)
        assert len(result) == 1024

    def test_cohere_embed_query_uses_search_query_type(self, mock_boto3_session, mock_bedrock_client):
        """Test that Cohere uses search_query input type for queries."""
        from vectorstore_unified.embeddings import BedrockEmbeddings

        embeddings = BedrockEmbeddings(model_id="cohere.embed-english-v3")
        embeddings.embed_query("search query")

        # Check that invoke_model was called with search_query input_type
        call_args = mock_bedrock_client.invoke_model.call_args
        body = json.loads(call_args.kwargs.get("body", call_args[1].get("body", "{}")))
        assert body.get("input_type") == "search_query"

    def test_dimension_property(self, mock_boto3_session):
        """Test dimension property returns correct value."""
        from vectorstore_unified.embeddings import BedrockEmbeddings

        titan_v2 = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
        titan_v1 = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1")

        assert titan_v2.dimension == 1024
        assert titan_v1.dimension == 1536

    def test_unsupported_model_raises_error(self, mock_boto3_session):
        """Test that unsupported model raises ValueError."""
        from vectorstore_unified.embeddings import BedrockEmbeddings

        embeddings = BedrockEmbeddings(model_id="unsupported.model")

        with pytest.raises(ValueError, match="Unsupported model"):
            embeddings.embed_text("test")


class TestOpenAIEmbeddings:
    """Tests for OpenAI embeddings."""

    def test_embed_text(self):
        """Test embedding single text with OpenAI."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("openai.OpenAI") as mock_openai:
                # Setup mock
                mock_client = MagicMock()
                mock_openai.return_value = mock_client
                mock_client.embeddings.create.return_value = MagicMock(
                    data=[MagicMock(embedding=[0.1] * 1536)]
                )

                from vectorstore_unified.embeddings import OpenAIEmbeddings

                embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
                result = embeddings.embed_text("Hello world")

                assert len(result) == 1536

    def test_embed_texts_batched(self):
        """Test that embed_texts uses batched API."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("openai.OpenAI") as mock_openai:
                mock_client = MagicMock()
                mock_openai.return_value = mock_client
                mock_client.embeddings.create.return_value = MagicMock(
                    data=[
                        MagicMock(embedding=[0.1] * 1536),
                        MagicMock(embedding=[0.2] * 1536),
                    ]
                )

                from vectorstore_unified.embeddings import OpenAIEmbeddings

                embeddings = OpenAIEmbeddings()
                results = embeddings.embed_texts(["Hello", "World"])

                assert len(results) == 2
                # Should only call API once (batched)
                assert mock_client.embeddings.create.call_count == 1

    def test_missing_api_key_raises_error(self):
        """Test that missing API key raises ValueError."""
        with patch.dict("os.environ", {}, clear=True):
            # Remove OPENAI_API_KEY if it exists
            import os
            os.environ.pop("OPENAI_API_KEY", None)

            from vectorstore_unified.embeddings import OpenAIEmbeddings

            with pytest.raises(ValueError, match="API key required"):
                OpenAIEmbeddings()

    def test_dimension_property(self):
        """Test dimension property for different models."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("openai.OpenAI"):
                from vectorstore_unified.embeddings import OpenAIEmbeddings

                small = OpenAIEmbeddings(model="text-embedding-3-small")
                large = OpenAIEmbeddings(model="text-embedding-3-large")

                assert small.dimension == 1536
                assert large.dimension == 3072


class TestCohereEmbeddings:
    """Tests for Cohere embeddings."""

    def test_embed_text(self):
        """Test embedding single text with Cohere."""
        with patch.dict("os.environ", {"COHERE_API_KEY": "test-key"}):
            with patch("cohere.Client") as mock_cohere:
                mock_client = MagicMock()
                mock_cohere.return_value = mock_client
                mock_client.embed.return_value = MagicMock(
                    embeddings=[[0.1] * 1024]
                )

                from vectorstore_unified.embeddings import CohereEmbeddings

                embeddings = CohereEmbeddings()
                result = embeddings.embed_text("Hello world")

                assert len(result) == 1024

    def test_embed_query_uses_search_query_type(self):
        """Test that embed_query uses search_query input type."""
        with patch.dict("os.environ", {"COHERE_API_KEY": "test-key"}):
            with patch("cohere.Client") as mock_cohere:
                mock_client = MagicMock()
                mock_cohere.return_value = mock_client
                mock_client.embed.return_value = MagicMock(
                    embeddings=[[0.1] * 1024]
                )

                from vectorstore_unified.embeddings import CohereEmbeddings

                embeddings = CohereEmbeddings()
                embeddings.embed_query("search query")

                # Check input_type argument
                call_kwargs = mock_client.embed.call_args.kwargs
                assert call_kwargs.get("input_type") == "search_query"

    def test_dimension_property(self):
        """Test dimension property for different models."""
        with patch.dict("os.environ", {"COHERE_API_KEY": "test-key"}):
            with patch("cohere.Client"):
                from vectorstore_unified.embeddings import CohereEmbeddings

                english = CohereEmbeddings(model="embed-english-v3.0")
                light = CohereEmbeddings(model="embed-english-light-v3.0")

                assert english.dimension == 1024
                assert light.dimension == 384
