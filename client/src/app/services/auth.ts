// auth.service.ts
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { jwtDecode, JwtPayload } from 'jwt-decode';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { host } from '../constant';

@Injectable({ providedIn: 'root' })
export class AuthService {
private apiUrl = `${host}`;
  constructor(private router: Router,private http:HttpClient) {
  }


//Login Method:
login(loginData: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login`, loginData).pipe(
      tap(res => {
        if (res.token) { // API'den gelen token alanı adını kontrol et (genelde 'token' veya 'accessToken' olur)
          localStorage.setItem("token", res.token);
        }
      })
    );
  }


  // Token'ı localStorage'dan al -> ocalStorage is not defined engellemek:
getToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem("token");
  }
  return null;
}
  isAuthenticated(): boolean {
    const token = this.getToken();
    if (token) {
      try {
        const decode: any = jwtDecode(token);
        const now = new Date().getTime() / 1000;
        
        // Token süresi dolmuş mu?
        if (now > decode.exp) {
          this.logout();
          return false;
        }
        return true;
      } catch (error) {
        this.logout();
        return false;
      }
    }
    this.router.navigateByUrl("/login");
    return false;
  }

  logout() {
    localStorage.removeItem("token");
    this.router.navigateByUrl("/login");
  }
}