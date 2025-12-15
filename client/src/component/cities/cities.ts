// 1. Gerekli modülü import edin (yolu kendi projenize göre ayarlayın)
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';


@Component({
  selector: 'app-cities',
  standalone: true, // Bileşen standalone ise
  imports: [
    RouterLink,

  ],
  templateUrl: './cities.html',
  styleUrl: './cities.css',
})
export class Cities {
  

  search: string = ''; 



}
