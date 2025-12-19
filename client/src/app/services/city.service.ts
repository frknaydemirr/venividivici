import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { City, CityListResponse } from '../../models/city.model';
import { Question } from '../../models/questions.model';


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
//City comes with special Id -> When city cliked for  (detail page)
  getCityById(CityId:Number):Observable<City>{
    return this.http.get<City>(`${this.apiUrl}/${CityId}`);
  }


// Şehir sayfasındaki istatistikler için
getCityCounts(cityId: number): Observable<{ 'question-count': number, 'answer-count': number }> {
  return this.http.get<any>(`${this.apiUrl}/cities/${cityId}/counts`);
}

// Şehir bazlı sorular için
getRecentQuestionsByCity(cityId: number): Observable<Question[]> {
  return this.http.get<Question[]>(`${this.apiUrl}/questions/recent/by-city/${cityId}`);
}

}
