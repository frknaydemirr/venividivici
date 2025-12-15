import { Component, OnInit } from '@angular/core';
import { City } from '../../models/city.model';
import { Country } from '../../models/country.model';
import { CityService } from '../../app/services/city.service';
import { CountryService } from '../../app/services/country.service';

@Component({
  selector: 'app-home',
  imports: [],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {

  // Şehirler için veriler ve sayfalama bilgileri
  mostConqueredCities: City[] = [];
  cityOffset=0;
  cityLimit=5;
  hasMoreCities=true;
// Ülkeler için veriler
  mostConqueredCountries: Country[] = [];

  constructor(
  private cityService: CityService, 
  private countryService: CountryService

  ) {}

ngOnInit() : void{
    this.loadMostConqueredCities();
    this.loadMostConqueredCountries();
  }

  //cities
loadMostConqueredCities(): void {
    if (!this.hasMoreCities) return;

    this.cityService.getMostConqueredCities(this.cityOffset, this.cityLimit)
      .subscribe({
        next: (newCities: City[]) => {
          this.mostConqueredCities = [...this.mostConqueredCities, ...newCities];
          
          if (newCities.length < this.cityLimit) {
            this.hasMoreCities = false; // Son sayfadayız
          }
          this.cityOffset += this.cityLimit; // Bir sonraki sayfanın başlangıcını ayarla
        },
        error: (err) => console.error('Most Conquered Cities yüklenirken hata oluştu:', err)
      });
  }

//countries
loadMostConqueredCountries(): void {
    this.countryService.getMostConqueredCountries()
      .subscribe({
        next: (countries: Country[]) => {
          this.mostConqueredCountries = countries; 
        },
        error: (err) => console.error('Most Conquered Countries yüklenirken hata oluştu:', err)
      });
  }



}
