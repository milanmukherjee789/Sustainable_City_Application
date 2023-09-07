import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
import { User } from './../model/user';
import { LoginResult } from '../model/login_result';
import { hostname } from '../model/constants';

@Injectable({ providedIn: 'root' })
export class AccountService {
    private userSubject: BehaviorSubject<User | null>;
    public user: Observable<User | null>;

    constructor(
        private router: Router,
        private http: HttpClient
    ) {
        this.userSubject = new BehaviorSubject(JSON.parse(localStorage.getItem('user')!));
        this.user = this.userSubject.asObservable();
    }

    public get userValue() {
        return this.userSubject.value;
    }

    login(username: string, password: string): Observable<boolean> {
        
        return this.http.post<LoginResult>('http://' + hostname + ':5000/request/authenticate', { userName: username, passWord: password })
            .pipe(map(result => {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                console.log(result);
                if(result.authorized) {
                    localStorage.setItem('token', result?.token);
                    localStorage.setItem('user', JSON.stringify({ userName: username, passWord: password }));
                    this.userSubject.next({ userName: username, passWord: password });
                    return true;
                } else {
                    return false;
                }
            }));
    }

    
    logout() {
        localStorage.removeItem('user');
        this.userSubject.next(null);
        this.router.navigate(['/account/login']);
    }

    getById(id: string) {
        return this.http.get<User>('http://' + hostname + ':5000/request/allUsers'+'/users/${id}');
    }

    update(id: string, params: any) {
        return this.http.put('http://' + hostname + ':5000/request/allUsers'+'/users/${id}', params)
            .pipe(map(x => {
                // update stored user if the logged in user updated their own record
                if (id == this.userValue?.id) {
                    // update local storage
                    const user = { ...this.userValue, ...params };
                    localStorage.setItem('user', JSON.stringify(user));

                    // publish updated user to subscribers
                    this.userSubject.next(user);
                }
                return x;
            }));
    }
    
}