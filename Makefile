
GOROOT := ../../../


protobuf:

	# Preflight
	mkdir -p server/proto/v1/response \
			 server/proto/v1/tracker

	mkdir -p client/proto

	touch server/proto/__init__.py \
		server/proto/v1/__init__.py \
	 	server/proto/v1/tracker/__init__.py \
		server/proto/v1/response/__init__.py

	# Generate code
	# Server:
	python3 -m grpc_tools.protoc -Iservice/ \
		    --python_out=server/ \
			--grpc_python_out=server/ \
		    service/proto/v1/response/*.proto \
		    service/proto/v1/tracker/*.proto

	# Console:
	python3 -m grpc_tools.protoc -Iservice/ \
		    --python_out=console/ \
			--grpc_python_out=server/ \
		    service/proto/v1/response/*.proto \
		    service/proto/v1/tracker/*.proto

	# Client:
	protoc -I service/ --go_out=plugins=grpc:$(GOROOT) \
		    service/proto/v1/tracker/*.proto

	protoc -I service/ --go_out=plugins=grpc:$(GOROOT) \
		    service/proto/v1/response/*.proto \

