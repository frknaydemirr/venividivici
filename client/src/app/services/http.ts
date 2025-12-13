import { Injectable } from '@angular/core';
import { Auth } from './auth';
import { Error } from './error';
import { api } from '../constant'; 
import { ResultModel } from '../../models/result.model';
import { HttpErrorResponse } from '@angular/common/http';
 

@Injectable({
  providedIn: 'root',
})
export class Http {
 
  constructor(
private http: Http,
private auth: Auth,
private error: Error

  ) { }


//Generic Post yapısı:

// post<T>(apiUrl:string,body:any,callBack:(res:T)=>void,errorCallBack?:()=>void){
//   this.http.post<ResultModel<T>>(`${api}/${apiUrl}`,body,{
//     headers:{
//       "Authorization": "Bearer " + this.auth.token
//     }
//   }).subscribe({
//     next:(res)=>{
//       if(res.data){
//          callBack(res.data);
//       }
//     },
//     error:(err:HttpErrorResponse)=>{
//       this.error.errorHandler(err);
//       if(errorCallBack){
//         errorCallBack();
//       }
//     }
//   });

// }

}