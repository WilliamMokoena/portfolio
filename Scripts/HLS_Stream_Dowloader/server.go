package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	// define the directory of the media and port to host it on
	const media = "site"
	const port = 8000

	// add a handler for the song files
	http.Handle("/", addHeaders(http.FileServer(http.Dir(media))))
	fmt.Printf("Starting server on %v\n", port)
	log.Printf("Serving %s on HTTP port: %v\n", media, port)

	// serve and log errors
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%v", port), nil))
}

// addHeaders will act as middleware to give us CORS support
func addHeaders(h http.Handler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		h.ServeHTTP(w, r)
	}
}
