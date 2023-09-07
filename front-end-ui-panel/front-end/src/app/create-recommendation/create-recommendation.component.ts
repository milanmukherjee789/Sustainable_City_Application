import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs/internal/observable/of';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Subject, first, map } from 'rxjs';
import { ActivatedRoute, Router } from '@angular/router';
import { AccountService, AlertService } from '../service';
import { ReactiveFormsModule } from '@angular/forms';
import { Recommendation } from '../model/recommendation';

@Component({
  selector: 'createrecommendation',
  templateUrl: './create-recommendation.component.html',
  styleUrls: ['./create-recommendation.component.scss']
})
export class CreateRecommendationComponent {
  
  loading = false;
createform: FormGroup<any> = new FormGroup({
  incident: new FormControl(),
  location: new FormControl(),
  message: new FormControl(),
});
errorHidden$: Subject<boolean> = new Subject<boolean>();
submitted = false;
constructor(
  private formBuilder: FormBuilder,
  private route: ActivatedRoute,
  private router: Router,
  private accountService: AccountService,
  private alertService: AlertService,
  private http: HttpClient,
) { 

}
  ngOnInit() {
  }
     // convenience getter for easy access to form fields
     get f() { return this.createform.controls; }

createRecommendation() {
  this.submitted = true;
  // stop here if form is invalid
  if (this.createform.invalid) {
      return;
  }
  this.loading = true;
console.log(48);
  // reset alerts on submit
  this.alertService.clear();
  console.log(51);
  this.http.post<Recommendation>('http://10.6.48.170:5000/recommendations/create', { location: this.f['location'].value, message: this.f['message'].value , incident: this.f['incident'].value })
            .pipe(map(result => {
              
console.log(54);
                this.loading = false;
                console.log(result);
            }));
  

}

}
