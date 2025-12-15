import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CountryListResponse } from '../../models/country.model';

@Injectable({
  providedIn: 'root',
})
export class CountryService {
  private apiUrl = 'https://api.example.com/countries';

  constructor(private http:HttpClient) {}
getMostConqueredCountries(): Observable<CountryListResponse> {
    return this.http.get<CountryListResponse>(`${this.apiUrl}/countries/most-conquered`);
  }
}
