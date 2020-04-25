import { Component, OnInit, ViewChild } from '@angular/core';
import { IgxCarouselComponent } from 'igniteui-angular';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {

  constructor() { }

  @ViewChild('carousel', { static: true }) public carousel: IgxCarouselComponent;

  public slides: any[] = [];
  public animations = ['slide', 'fade', 'none'];

  public ngOnInit() {
    this.addSlides();
  }

  public addSlides() {
    this.slides.push(
      {
        description: 'Centro de Investigación y Análisis de Datos',
        heading: 'CIAD',
        image: './assets/img/image.jpg',
        link: 'https://www.infragistics.com/products/ignite-ui-angular',
      },
      {
        description: 'Informática Forense',
        heading: 'CIAD',
        image: './assets/img/image1.jpg',
        link: 'https://www.infragistics.com/products/ignite-ui',
      },
      {
        description: 'Desarrollo de software',
        heading: 'CIAD',
        image: './assets/img/image2.jpg',
        link: 'https://www.infragistics.com/products/aspnet',
      },
    );
  }

}
