up-db:
	docker compose up -d
	
migrate-up:
	docker run -v ./:/migrations --network host migrate/migrate \
    	-path=/migrations/ -database postgres://postgres:postgres@localhost:5432/teamdev?sslmode=disable up 

migrate-down:
	echo "y" | docker run -v ./:/migrations --network host migrate/migrate \
		-path=/migrations/ -database postgres://postgres:postgres@localhost:5432/teamdev?sslmode=disable down -all 