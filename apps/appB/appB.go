package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "<p><hr><center> Service B</center></p>")
		log.Printf("%s %s %s\n", r.RemoteAddr, r.Method, r.URL)
	})

	log.Fatal(
		http.ListenAndServe(":8888", nil),
	)

}
