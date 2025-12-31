import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { SwalService } from './swal.service';

@Injectable({
  providedIn: 'root'
})
export class Error {
  constructor(
    private swal: SwalService
  ){}


errorHandler(err:HttpErrorResponse){
  debugger
  console.log(err);
  let message="Error";
  if(err.status===0){
     message="API is not available ","error";
  }else if(err.status===401){
    message="You're not authorized"
  }
  
  else if(err.status===404){
     message= "API is not found ","error";
  }else if(err.status===500){
    message="";
    for(const e of err.error.errorMessages){
      message+=e + "\n";
    }
  }

  this.swal.callToast(message,"error");
}

}


