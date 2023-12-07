# # Source the .env file to export environment variables
# if [ -f ".env" ]; then
#     echo "Exporting env variables"
#     export $(cat .env | xargs)
# fi


# mc alias remove s3storage
# echo 'Alias minio'
# mc alias set s3storage ${MINIO_ENDPOINT} ${MINIO_ACCESS_KEY_ID} ${MINIO_SECRET_KEY}
# echo 'Create bucket'
# mc mb s3storage/${MINIO_BUCKET_NAME}

echo 'Alias minio'
mc alias set s3storage http://127.0.0.1:9000 obai9Szm6zF7XpWr6UTQ vNZBQjoCigmI6QDhMIG2BQhm6Vgx4WFGqQkhAdZ4
echo 'Create bucket'
mc mb s3storage/models

echo "Init dvc"
dvc init -f
dvc remote remove s3storage
dvc remote add -d s3storage s3://models -f
dvc remote modify s3storage endpointurl http://127.0.0.1:9000
dvc remote modify s3storage access_key_id obai9Szm6zF7XpWr6UTQ
dvc remote modify s3storage secret_access_key vNZBQjoCigmI6QDhMIG2BQhm6Vgx4WFGqQkhAdZ4