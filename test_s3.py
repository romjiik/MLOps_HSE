import pytest
import boto3


# Инициализация клиента boto3 для S3
s3_client = boto3.client('s3',
                        endpoint_url='http://127.0.0.1:9000',
                        aws_access_key_id='obai9Szm6zF7XpWr6UTQ',
                        aws_secret_access_key='vNZBQjoCigmI6QDhMIG2BQhm6Vgx4WFGqQkhAdZ4',
                        verify=False  # Для отключения проверки SSL-сертификата
)


@pytest.fixture(scope="function")
def test_bucket():
    # Создание тестового бакета в MinIO
    bucket_name = "test"
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        yield bucket_name
    finally:
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name)
            if "Contents" in response:
                objects = [{"Key": obj["Key"]} for obj in response["Contents"]]
                s3_client.delete_objects(Bucket=bucket_name, Delete={"Objects": objects})
            s3_client.delete_bucket(Bucket=bucket_name)
        except s3_client.exceptions.NoSuchBucket:
            pass


def test_create_and_delete_bucket(test_bucket):
    # Проверка создания и удаления бакета в MinIO
    response = s3_client.list_buckets()
    bucket_names = [bucket["Name"] for bucket in response["Buckets"]]
    assert test_bucket in bucket_names

    try:
        s3_client.delete_bucket(Bucket=test_bucket)
        response = s3_client.list_buckets()
        bucket_names = [bucket["Name"] for bucket in response["Buckets"]]
        assert test_bucket not in bucket_names
    except s3_client.exceptions.NoSuchBucket:
        pass


def test_upload_and_download_file(test_bucket):
    # Загрузка и загрузка файла в бакет MinIO
    file_name = "test_file.txt"
    file_content = b"Test file content"

    try:
        # Загрузка файла в бакет
        s3_client.put_object(Bucket=test_bucket, Key=file_name, Body=file_content)

        # Проверка, что файл существует в бакете
        response = s3_client.list_objects_v2(Bucket=test_bucket, Prefix=file_name)
        assert "Contents" in response
        assert any(obj["Key"] == file_name for obj in response["Contents"])

        # Скачивание файла из бакета
        response = s3_client.get_object(Bucket=test_bucket, Key=file_name)
        downloaded_content = response["Body"].read()

        # Проверка, что содержимое скачанного файла совпадает с загруженным содержимым
        assert downloaded_content == file_content

        # Удаление файла из бакета
        s3_client.delete_object(Bucket=test_bucket, Key=file_name)

        # Проверка, что файл больше не существует в бакете
        with pytest.raises(s3_client.exceptions.NoSuchKey):
            s3_client.get_object(Bucket=test_bucket, Key=file_name)

    except s3_client.exceptions.S3Exception as e:
        assert False, str(e)



