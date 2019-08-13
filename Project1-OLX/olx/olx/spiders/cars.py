# -*- coding: utf-8 -*-
import scrapy


class CarsSpider(scrapy.Spider):
    name = 'cars'
    allowed_domains = ['pi.olx.com.br']
    start_urls = ['http://pi.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/']

    def parse(self, response):
        '''        
        items = response.xpath(
            '//ul[@id="main-ad-list"]/li[contains(@class, "item") and not(contains(@class, "list_native"))]'
        )
        '''
        items = response.xpath(
            '//ul[@id="main-ad-list"]/li[not(contains(@class, "list_native"))]'
        )
        self.log(len(items))
        for item in items:
            url = item.xpath('.//a/@href').extract_first()

            yield scrapy.Request(
                url=url,
                callback=self.parse_detail
            )
        next_page = response.xpath('//div[contains(@class, "module_pagination")]//a[@rel="next"]/@href')
        if next_page:
            self.log('Próxima página: {}'.format(next_page.extract_first()))
            yield scrapy.Request(
                url=next_page.extract_first(),
                callback=self.parse
            )

    def parse_detail(self, response):
        title = response.xpath('//title/text()').extract_first()
        categorical = response.xpath('//span[contains(text(), "Categoria")]/following-sibling::strong/a/@title').extract_first()
        model = response.xpath('//span[contains(text(), "Modelo")]/following-sibling::strong/a/@title').extract_first()
        motor_power = response.xpath('//span[contains(text(), "Potência do motor")]/following-sibling::strong/text()').extract_first()
        doors = response.xpath('//span[contains(text(), "Portas")]/following-sibling::strong/text()').extract_first()
        plate_end = response.xpath('//span[contains(text(), "Final de placa")]/following-sibling::strong/text()').extract_first()
        type_vehicle = response.xpath('//span[contains(text(), "Tipo de veículo")]/following-sibling::strong/text()').extract_first()
        year = response.xpath('//span[contains(text(), "Ano")]/following-sibling::strong/a/@title').extract_first()
        fuel = response.xpath('//span[contains(text(), "Combustível")]/following-sibling::strong/a/@title').extract_first()
        mileage = response.xpath('//span[contains(text(), "Quilometragem")]/following-sibling::strong/text()').extract_first()
        exchange = response.xpath('//span[contains(text(), "Câmbio")]/following-sibling::strong/text()').extract_first()
        direction = response.xpath('//span[contains(text(), "Direção")]/following-sibling::strong/text()').extract_first()
        color = response.xpath('//span[contains(text(), "Cor")]/following-sibling::strong/text()').extract_first()
        only_owner = response.xpath('//span[contains(text(), "Único dono")]/following-sibling::strong/text()').extract_first()
        accept_exchanges = response.xpath('//span[contains(text(), "Aceita Trocas")]/following-sibling::strong/text()').extract_first()
        options = response.xpath('//ul[contains(@class, "OLXad-features-list")]/li/text()').extract()

        mileage = ''.join(mileage.split())

        options = '-'.join(options)
        options = ', '.join(options.split('-'))

        yield {
            'title': title,
            'categorical': categorical,
            'model': model,
            'motor_power': motor_power,
            'doors': doors,
            'plate_end': plate_end,
            'type_vehicle': type_vehicle,
            'year': year,
            'fuel': fuel,
            'mileage': mileage,
            'exchange': exchange,
            'direction': direction,
            'color': color,
            'only_owner': only_owner,
            'accept_exchanges': accept_exchanges,
            'options': options,
        }