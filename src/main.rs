extern crate imgur;

mod uploader;

use std::fs::File;
use std::io::Read;

fn main() {
    let args = &mut std::env::args();
    let id = args.nth(1).expect("Need a client ID as argument");
    let mut file = File::open("test.jpg").expect("Could not open test.jpg");

    let mut data = Vec::new();
    file.read_to_end(&mut data).expect("Could not read image file");


    match uploader::upload(id, &data) {
        Ok(info) => {
            match info.link() {
                Some(link) => println!("Image uploaded successfully to {}", link),
                None => println!("You shouldn't ever see this."),
            }
        }
        Err(e) => {
            println!("Error uploading: {}", e);
        }
    }
}
