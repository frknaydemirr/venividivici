import { Component } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';import { Route } from '@angular/router';

@Component({
  selector: 'app-navbar',
  imports: [RouterOutlet],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar {

constructor(
private router:Router
) {
 }



}
