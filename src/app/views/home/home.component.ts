import { Component, OnInit, ViewChild } from '@angular/core';
import { IgxCarouselComponent } from 'igniteui-angular';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
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
        description: '30+ Material-based Angular components to code speedy web apps faster.',
        heading: 'Ignite UI for Angular',
        image: './assets/img/image.jpg',
        link: 'https://www.infragistics.com/products/ignite-ui-angular'
      },
      {
        description: 'A complete JavaScript UI library empowering you to build data-rich responsive web apps.',
        heading: 'Ignite UI for Javascript',
        image: './assets/img/image1.jpg',
        link: 'https://www.infragistics.com/products/ignite-ui'
      },
      {
        description: 'Build full-featured business apps with the most versatile set of ASP.NET AJAX UI controls',
        heading: 'Ultimate UI for ASP.NET',
        image: './assets/img/image2.jpg',
        link: 'https://www.infragistics.com/products/aspnet'
      }
    );
  }

}
