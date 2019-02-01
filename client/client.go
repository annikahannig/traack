package main

import (
	"context"
	"fmt"
	"log"
	"time"

	tracker_pb "github.com/mhannig/traack/service/lib/v1/tracker"
	"google.golang.org/grpc"
)

func main() {
	fmt.Println("traak v1")

	// Set up a connection to the server.
	conn, err := grpc.Dial("localhost:2344", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	// Create client
	customers_svc := tracker_pb.NewCustomerServiceClient(conn)

	// Make request
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	res, err := customers_svc.CreateCustomer(ctx, &tracker_pb.CreateCustomerRequest{
		Customer: &tracker_pb.Customer{
			Name: "Fnordbert.",
		},
	})
	if err != nil {
		log.Println(err)
	}

	fmt.Println("Result:")
	fmt.Println(res)

	res, err = customers_svc.CreateCustomer(ctx, &tracker_pb.CreateCustomerRequest{
		Customer: &tracker_pb.Customer{
			Name: "Ft",
		},
	})
	if err != nil {
		log.Println(err)
	}

	fmt.Println("Result:")
	fmt.Println(res)

	res, err = customers_svc.CreateCustomer(ctx, &tracker_pb.CreateCustomerRequest{
		Customer: &tracker_pb.Customer{
			Name: "",
		},
	})
	if err != nil {
		log.Println(err)
	}

	fmt.Println("Result:")
	fmt.Println(res)
}
