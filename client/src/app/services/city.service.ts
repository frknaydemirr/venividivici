import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CityListResponse } from '../../models/city.model';


@Injectable({
  providedIn: 'root',
})
export class CityService {
  private apiUrl = 'https://api.example.com/cities';

  constructor(private http:HttpClient) {}


  //En Çok Fethedilen şehirtleri getirme:

  getMostConqueredCities(offset: number, limit: number):Observable<CityListResponse>{
    const params = new HttpParams()
      .set('offset', offset.toString())
      .set('limit', limit.toString());

      return this.http.get<CityListResponse>(`${this.apiUrl}/cities/most-conquered`, { params });


  }
  
}
