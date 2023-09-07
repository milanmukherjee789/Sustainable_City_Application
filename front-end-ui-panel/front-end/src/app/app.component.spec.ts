import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';

import { ComponentFixture } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';


describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [
        AppComponent
      ],
      imports: [
        HttpClientModule,  
        RouterTestingModule,
      ],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the app', () => {
    expect(component).toBeTruthy();
  });

  it('should toggle the hamburger menu', () => {
    component.toggleCollapse();
    expect(component.hamburger_toggled).toBe(true);
  });

  it('should create the app', () => {
    expect(component).toBeTruthy();
  });

  it(`should have as title 'front-end'`, () => {
    expect(component.title).toEqual('front-end');
  });

  it('should render title', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Smart City Management Dashboard');
  });

  
  it('should show map', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const hamburger_map = fixture.debugElement.nativeElement.querySelector('#hamburger-map');
    console.log(hamburger_map)
    hamburger_map.click();
    const map_object = fixture.debugElement.nativeElement.querySelector('.map-container');
    console.log(map_object);
    expect(map_object.visible);
  });
});
