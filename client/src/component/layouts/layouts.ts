import { Component } from '@angular/core';
import { Navbar } from "../navbar/navbar";
import { RouterOutlet } from "@angular/router";
import { Footer } from "../footer/footer";

@Component({
  selector: 'app-layouts',
  imports: [Navbar, RouterOutlet, Footer],
  templateUrl: './layouts.html',
  styleUrl: './layouts.css',
})
export class Layouts {

}
