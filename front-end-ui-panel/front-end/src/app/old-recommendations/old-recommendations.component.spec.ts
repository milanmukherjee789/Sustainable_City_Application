import { HttpClientModule } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OldRecommendationsComponent } from './old-recommendations.component';

describe('OldRecommendationsComponent', () => {
  let component: OldRecommendationsComponent;
  let fixture: ComponentFixture<OldRecommendationsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OldRecommendationsComponent ],
      imports: [
        HttpClientModule,  
      ],
    })
    .compileComponents();

    fixture = TestBed.createComponent(OldRecommendationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should show the component', () => {
    expect(component).toBeTruthy();
  });
  it('should call fetchRecommendations on ngOnInit', () => {
    spyOn(component, 'fetchRecommendations');

    component.ngOnInit();

    expect(component.fetchRecommendations).toHaveBeenCalled();
  });
});
