import pytest


@pytest.fixture
def mock_storage_client(mocker):
    mocker.patch('storage.StorageClient._conn_str', "fake_connection_string")

    mock_blob_client = mocker.Mock()
    mock_blob_client.exists.return_value = False

    mock_blob_service_instance = mocker.Mock()
    mock_blob_service_instance.get_blob_client.return_value = mock_blob_client

    mock_blob_service = mocker.patch("storage.BlobServiceClient")
    mock_blob_service.from_connection_string.return_value = mock_blob_service_instance

    from storage import StorageClient
    return StorageClient(), mock_blob_client


def test_generate_blob_filename(mock_storage_client):
    storage_client, _ = mock_storage_client
    filename = "example.txt"
    result = storage_client._generate_blob_filename(filename)
    assert result.endswith(".txt")
    assert len(result.split(".")) == 2


def test_upload_blob_new_blob(mock_storage_client):
    storage_client, mock_blob_client = mock_storage_client

    storage_client.upload_blob(b"data", "container", "file.txt")

    mock_blob_client.upload_blob.assert_called_once_with(
        b"data", blob_type="BlockBlob", metadata={"filename": "file.txt"}
    )


def test_upload_blob_existing_blob(mock_storage_client):
    storage_client, mock_blob_client = mock_storage_client
    mock_blob_client.exists.return_value = True

    storage_client.upload_blob(b"data", "container", "file.txt")
    mock_blob_client.upload_blob.assert_not_called()
