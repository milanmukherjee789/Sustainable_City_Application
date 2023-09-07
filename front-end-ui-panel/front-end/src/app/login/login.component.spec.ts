import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterTestingModule } from '@angular/router/testing';
import { AccountService, AlertService } from '../service';
import { LoginComponent } from './login.component';
import { of } from 'rxjs';
import { Map2Component } from '../map2/map2.component';
import { OldRecommendationsComponent } from '../old-recommendations/old-recommendations.component';
import { CreateRecommendationComponent } from '../create-recommendation/create-recommendation.component';
import { LandingPageComponent } from '../landing-page/landing-page.component';
import { RecommendationComponent } from '../recommendation/recommendation.component';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;
  let mockAccountService: jasmine.SpyObj<AccountService>;
  let mockAlertService: jasmine.SpyObj<AlertService>;

  beforeEach(async () => {
    mockAccountService = jasmine.createSpyObj('AccountService', ['login']);
    mockAlertService = jasmine.createSpyObj('AlertService', ['clear']);

    await TestBed.configureTestingModule({
      imports: [ReactiveFormsModule, RouterTestingModule, RouterTestingModule.withRoutes([
        {path: '',   redirectTo: '/login', pathMatch: 'full'},
        {path: 'login', component: LoginComponent},
        {path: 'landing-page', component: LandingPageComponent},
        {path: 'recommendation', component: RecommendationComponent},
        {path: 'old-recommendations', component: OldRecommendationsComponent},
        {path: 'create-recommendation', component: CreateRecommendationComponent},
        {path: 'map2', component: Map2Component},
      
      ])],
      declarations: [LoginComponent],
      providers: [
        { provide: AccountService, useValue: mockAccountService },
        { provide: AlertService, useValue: mockAlertService }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();

  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should clear alerts on submit', () => {
    mockAccountService.login.and.returnValue(of(true));
    component.onSubmit();
    expect(mockAlertService.clear).toHaveBeenCalled();
  });
  it('should set submitted to true on submit', () => {
    mockAccountService.login.and.returnValue(of(true));
    component.onSubmit();
    expect(component.submitted).toBeTrue();
  });
  
  it('should not call accountService.login if form is invalid', () => {
    mockAccountService.login.and.returnValue(of(false));
    component.loginform.setErrors({ invalid: true });
    component.onSubmit();
    expect(mockAccountService.login).not.toHaveBeenCalled();
  });
  
  it('should call accountService.login with username and password if form is valid', () => {
    
    mockAccountService.login.and.returnValue(of(true));
    component.f['username'].setValue('testuser');
    component.f['password'].setValue('testpass');
    component.onSubmit();
    expect(mockAccountService.login).toHaveBeenCalledWith('testuser', 'testpass');
  });
  it('should have invalid loginform when username and password fields are empty', () => {
    mockAccountService.login.and.returnValue(of(false));
    expect(component.loginform.valid).toBeFalsy();
  });

  it('should have valid loginform when username and password fields are filled with valid values', () => {
    mockAccountService.login.and.returnValue(of(true));
    component.loginform.controls['username'].setValue('testuser');
    component.loginform.controls['password'].setValue('testpass');
    expect(component.loginform.valid).toBeTruthy();
  });

  it('should call onSubmit() method when form is submitted', () => {
    spyOn(component, 'onSubmit');
    mockAccountService.login.and.returnValue(of(true));
    let form = fixture.debugElement.nativeElement.querySelector('form');
    form.dispatchEvent(new Event('submit'));
    expect(component.onSubmit).toHaveBeenCalled();
  });

  it('should call alertService.clear() method when form is submitted', () => {
    component.onSubmit();
    mockAccountService.login.and.returnValue(of(true));
    expect(mockAlertService.clear).toHaveBeenCalled();
  });

  it('should call accountService.login() method with correct parameters when form is submitted with valid values', () => {
    mockAccountService.login.and.returnValue(of(true));
    component.loginform.controls['username'].setValue('testuser');
    component.loginform.controls['password'].setValue('testpass');
    component.onSubmit();
    expect(mockAccountService.login).toHaveBeenCalledWith('testuser', 'testpass');
  });
});