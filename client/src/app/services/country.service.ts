import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CountryListResponse } from '../../models/country.model';
import { host } from '../constant';

@Injectable({
  providedIn: 'root',
})
export class CountryService {
  // host değişkeni sonuna '/' koymuyorsa `${host}/countries` kullanımı doğrudur.
  private apiUrl = `${host}/countries`;

  constructor(private http: HttpClient) {}

  /**
   * En çok fethedilen ülkeleri getirir.
   * Not: Eğer backend API'niz `${host}/countries/most-conquered` bekliyorsa 
   * aşağıdaki gibi direkt `${this.apiUrl}/most-conquered` kullanmalısınız.
   */
  getMostConqueredCountries(): Observable<CountryListResponse> {
    return this.http.get<CountryListResponse>(`${this.apiUrl}/most-conquered`);
  }

  // İleride ihtiyaç duyabileceğin örnek bir metod (ID'ye göre ülke getirme)
   getCountryById(countryId: number): Observable<any> {
     return this.http.get<any>(`${this.apiUrl}/${countryId}`);
   }

   //searchbox for country
   searchCountries(query: string): Observable<any[]> {
  return this.http.get<any[]>(`${host}/search/countries/${query}`);
}
}