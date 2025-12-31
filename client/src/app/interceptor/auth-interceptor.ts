import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // SSR (Server Side Rendering) kullanıyorsan window kontrolü eklemek güvenlidir
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

  if (token) {
    // Swagger'da tanımlanan 'api-key-header' ismini kullanıyoruz
    const cloned = req.clone({
      setHeaders: {
        'api-key-header': token 
      }
    });
    return next(cloned);
  }

  return next(req);
};