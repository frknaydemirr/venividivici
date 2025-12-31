import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Country } from '../../models/country.model';
import { CountryService } from '../../app/services/country.service';
import { SearchBoxComponent } from '../search.component/search.component';

@Component({
  selector: 'app-countries',
  standalone: true,
  imports: [CommonModule,SearchBoxComponent],
  templateUrl: './countries.html',
  styleUrl: './countries.css',
})
export class Countries implements OnInit {
  selectedCountry?: Country;
  isLoading: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private countryService: CountryService
  ) {}

  ngOnInit(): void {
    // URL'deki 'id' değişimlerini takip et
    this.route.params.subscribe(params => {
      const id = +params['id']; 
      if (id) {
        this.loadCountryDetails(id);
      }
    });
  }

  loadCountryDetails(id: number): void {
    this.isLoading = true;
    this.countryService.getCountryById(id).subscribe({
      next: (country: Country) => {
        this.selectedCountry = country;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('An Error occurred while country details loading', err);
        this.isLoading = false;
      }
    });
  }
}