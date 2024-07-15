import requests
from bs4 import BeautifulSoup
import lxml
import time
from os.path import exists

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import webdriver_manager
import pandas

list_of_urls = ['https://www.amainhobbies.com/', 'https://www.horizonhobby.com/', 'https://traxxas.com/',
                'http://hot-racing.com/']
# amainhobbies.com, horizonhobby.com, traxxas.com, hobbyrecreationproducts.com, hot-racing.com


driver = Chrome(service=Service(ChromeDriverManager().install()))

main_database = {}
user_input = input('which website do you want to scrape? or all')
# try:
if user_input == 'all':
    res = requests.get('https://www.amainhobbies.com/brands')
    all_product_urls = []
    print(len(BeautifulSoup(res.text, 'lxml').select('.branditem')))
    for item in (BeautifulSoup(res.text, 'lxml').select('.branditem')):
        try:
            all_product_urls.append(f'https://www.amainhobbies.com{item.select("a")[0].get("href")}')
        except:
            pass
    # driver = Chrome(service=Service(ChromeDriverManager().install()))

    for item in all_product_urls:
        try:
            # print('sdf')
            product_urls = []
            counter = 0
            while True:
                counter += 1
                print(f'{item}?p={counter}'.replace(' ', ''))
                response_of_brand_p = requests.get(f'{item}?p={counter}'.replace(' ', '')).text
                # print(response_of_brand_p)
                beautiful_brands = BeautifulSoup(response_of_brand_p, 'lxml')
                # print(beautiful_brands)
                # time.sleep(20)
                all_item_on_a_page = beautiful_brands.select('.product-image')
                for prod in all_item_on_a_page:
                    product_urls.append(prod.get('data-url'))
                if 'class="next"' in beautiful_brands.text:
                    pass
                else:
                    # print('brea')
                    break
            # print(product_urls)
            for url_of_p in product_urls:
                try:
                    driver.get(url_of_p)
                    time.sleep(3)
                    beautiful = BeautifulSoup(driver.page_source, 'lxml')
                    product_parent = beautiful.select('#product-info')[0]
                    # print(product_parent)
                    # time.sleep(40)
                    item_url_for_the_bot = url_of_p
                    product_name = product_parent.select_one('.sku').text
                    print(product_name)
                    product_description = product_parent.select_one('.productname').text.replace("\n", ' ')
                    product_long_description = beautiful.select('.tabs .tabcontent p')[0].text
                    print(product_long_description)
                    print(product_description)
                    try:
                        price_original = product_parent.select_one('.price s').text
                    except:
                        price_original = product_parent.select_one('.theprice td').text
                    print(price_original)
                    price_discounted = product_parent.select_one('.theprice td').text
                    print(price_discounted)
                    primary_image = product_parent.select('.mainphoto img')[0].get('src')
                    print(primary_image)
                    primary_vendor = product_parent.select('div .brandname span')[0].text
                    print(primary_vendor)
                    product_category = product_parent.select('.breadcrumb')[0].text.replace('\n', '')
                    raw_product_images_url = ''
                    for image_u in product_parent.select('.carousel img'):
                        raw_product_images_url += f", {image_u.get('src').replace('width=100', 'width=500')}"
                    product_images_url = raw_product_images_url[2:]
                    print(product_category)
                    print(product_images_url)
                    time.sleep(3)
                    main_database[product_name] = {'Item #': product_name,
                                                   'Description': product_description,
                                                   'Original Price': price_original,
                                                   'Current Price': price_discounted,
                                                   'Long Description': product_long_description,
                                                   'Primary Image': primary_image,
                                                   'Primary Vendor': primary_vendor,
                                                   'Category': product_category,
                                                   'Item Images URL': product_images_url,
                                                   "Item Url": item_url_for_the_bot,
                                                   'Scraped time details': time.asctime()
                                                   }
                    print(main_database, '-----------------------------------------------------------------------')
                except:
                    # pass
                    data_to_create_csv = {'Item #': [],
                                          'Description': [],
                                          'Original Price': [],
                                          'Current Price': [],
                                          'Long Description': [],
                                          'Primary Image': [],
                                          'Primary Vendor': [],
                                          'Category': [],
                                          'Item Images URL': [],
                                          "Item Url": []
                                          }

                    for ite in main_database:
                        for main in main_database[ite]:
                            data_to_create_csv[main].append(main_database[ite][main])

                    data_frame_pandas = pandas.DataFrame(data_to_create_csv)
                    data_frame_pandas.to_csv('scraped_data.csv')

        except:
            pass
            # except:
            #     # pass
            #     data_to_create_csv = {'Item #': [],
            #                           'Description': [],
            #                           'Original Price': [],
            #                           'Current Price': [],
            #                           'Long Description': [],
            #                           'Primary Image': [],
            #                           'Primary Vendor': [],
            #                           'Category': [],
            #                           'Item Images URL': [],
            #                           "Item Url": []
            #                           }
            #
            #     for ite in main_database:
            #         for main in main_database[ite]:
            #             data_to_create_csv[main].append(main_database[ite][main])

                # data_frame_pandas = pandas.DataFrame(data_to_create_csv)
                # data_frame_pandas.to_csv('amain_scraped_data.csv')
    # 'Item #': []
    # , 'Description': []
    # , 'Original Price': []
    # , 'Current Price': []
    # , 'Long Description': []
    # , 'Primary Image': []
    # , 'Primary Vendor': []
    # , 'Category': []
    # , 'Item Images URL': []
    # , "Item Url": []
    ree = requests.get('https://www.horizonhobby.com/brands/')
    # print(ree.text)

    links_of_brands = []

    beautiful_horizon = BeautifulSoup(ree.text, 'lxml')
    for item in beautiful_horizon.select('.card'):
        try:
            links_of_brands.append(item.select('a')[0].get('href').split('?')[0])
        except:
            pass


    # print(links_of_brands)

    for li in links_of_brands:
        try:
            counter_page = 0
            product_urls_hori = []
            while True:
                # if

                respoof_hori = requests.get(
                    f'{li}?prefn1=discontinued&prefv1=false&start={counter_page}&sz=100&return=true').text
                beautiful_horizon_prod = BeautifulSoup(respoof_hori, 'lxml')
                counter_page += 100
                if 'class="product-tile"' in respoof_hori:
                    pass
                else:
                    break
                raw_pro = beautiful_horizon_prod.select('.product-tile-img-container')
                for raw in raw_pro:
                    product_urls_hori.append(f'https://www.horizonhobby.com{raw.get("href")}')
                print(product_urls_hori)
            for prod in product_urls_hori:
                try:
                    driver.get(prod)
                    item_url_for_the_bot = [prod]
                    time.sleep(3)
                    beautiful = BeautifulSoup(driver.page_source, 'lxml')
                    product_parent = beautiful.select('.product-wrapper-a')[0]
                    # print(product_parent)
                    # time.sleep(40)
                    product_name = product_parent.select_one('.product-id').text
                    print(product_name)
                    if 'class="intro-block' not in driver.page_source:
                        product_description = product_parent.select_one('.product-name').text.replace('\n', '').replace('                                ', '')
                    else:
                        product_description = beautiful.select_one('.intro-block').text.replace('\n', '').replace(
                            '                                ', '')

                    if 'long-desc-content' not in driver.page_source:
                        product_long_description = product_description.replace('\n', '').replace(
                            '                                ', '')
                    else:
                        product_long_description = beautiful.select_one('.long-desc-content').select_one('p').text.replace(
                            '\n', '').replace('                                ', '')
                    print(product_long_description)
                    print(product_description)

                    try:
                        price_original = product_parent.select_one('.callout').text.replace('Was ', '').split('.')[
                            0].replace('\n', '').replace(' ', '')
                    except:
                        price_original = product_parent.select_one('.value').text.replace('\n', '').replace(' ', '')
                    print(price_original)
                    price_discounted = product_parent.select_one('.value').text.replace('\n', '').replace(' ', '')
                    print(price_discounted)
                    primary_image = product_parent.select('.slick-slide img')[0].get('src').replace('\n', '').replace(
                        '                                ', '')
                    print(primary_image)
                    primary_vendor = product_parent.select('.product-number .name-wrapper span')[0].text.replace('-',
                                                                                                                 '').replace(
                        '\n', '').replace('                                ', '')
                    print(primary_vendor)
                    product_category = product_parent.select('.breadcrumb')[0].text.replace('\n', '').replace(
                        '                                                    ', '>').replace('                            ',
                                                                                             '')
                    raw_product_images_url = ''
                    for image_u in product_parent.select('.slick-slide img')[1:]:
                        if "None" not in str(image_u.get('src')):
                            raw_product_images_url += f", {image_u.get('src')}"
                    product_images_url = raw_product_images_url[2:]
                    print(product_category)
                    print(product_images_url)
                    time.sleep(3)
                    main_database[product_name] = {'Item #': product_name,
                                                   'Description': product_description,
                                                   'Original Price': price_original,
                                                   'Current Price': price_discounted,
                                                   'Long Description': product_long_description,
                                                   'Primary Image': primary_image,
                                                   'Primary Vendor': primary_vendor,
                                                   'Category': product_category,
                                                   'Item Images URL': product_images_url,
                                                   "Item Url": item_url_for_the_bot,
                                                   'Scraped time details': time.asctime()
                                                   }
                except:
                    pass
        except:
            pass
    # beautiful_amain_temp = BeautifulSoup(requests.get('https://www.amainhobbies.com/').text, 'lxml').select('#parts-finder-vehicle option')[1:]
    # list_of_amain = []
    #
    # for item in beautiful_amain_temp:
    #     list_of_amain.append(f'https://www.amainhobbies.com{item.get("data-url")}')
    # # print(list_of_amain)
    # for item in list_of_amain:
    #     page_counter = 0
    #     product_urls_of_amain = []
    #     while True:
    #         page_counter += 1
    #         respo_of_amain_page = requests.get(f"{item}?p={page_counter}").text
    #         if 'No products found' in respo_of_amain_page:
    #             break
    #         else:
    #             pass
    #         beautiful_amain = BeautifulSoup(respo_of_amain, 'lxml')
    #         raw_url_of_amain = beautiful_amain.select('.product-image')
    #         for pro in raw_url_of_amain:
    #             product_urls_of_amain.append(pro.get('data-url'))
    #         print(product_urls_of_amain)
    #         time.sleep(1)
    #
    #     for pro_url in product_urls_of_amain:
    #         driver.get(pro_url)
    #         beautiful_amain_pro_page = BeautifulSoup(driver.page_source, 'lxml')
    #         # beautiful_amain_pro_page.select()
    #         product_name = product_parent.select_one('.productname').text
    #         print(product_name)
    #         product_description = product_name
    #         product_long_description = beautiful.select('.tabs .tabcontent p')[0].text
    #         print(product_long_description)
    #         print(product_description)
    #         try:
    #             price_original = product_parent.select_one('.price s').text
    #         except:
    #             price_original = product_parent.select_one('.theprice td').text
    #         print(price_original)
    #         price_discounted = product_parent.select_one('.theprice td').text
    #         print(price_discounted)
    #         primary_image = product_parent.select('.mainphoto img')[0].get('src')
    #         print(primary_image)
    #         primary_vendor = product_parent.select('div .brandname span')[0].text
    #         print(primary_vendor)
    #         product_category = product_parent.select('.breadcrumb')[0].text.replace('\n', '')
    #         raw_product_images_url = ''
    #         for image_u in product_parent.select('.carousel img'):
    #             raw_product_images_url += f", {image_u.get('src').replace('width=100', 'width=500')}"
    #         product_images_url = raw_product_images_url[2:]
    #         print(product_category)
    #         print(product_images_url)
    #         time.sleep(3)

    list_of_goto = ["https://traxxas.com/products/showroom", 'https://traxxas.com/products/parts/batteries-chargers']
    # driver.get().text
    # time.sleep(10)
    # print(driver.page_source)
    # for it in list_of_goto:
    driver.get(list_of_goto[0])
    beautiful_la = BeautifulSoup(driver.page_source, 'lxml')
    all_models = beautiful_la.select('.views-view-grid tbody tr td a')
    item_urls = []
    item_urls_landing = []
    cou = 0
    for item in all_models:
        cou += 1
        if 'landing' not in item.get('href') and f"https://traxxas.com{item.get('href')}" not in item_urls:
            item_urls.append(f"https://traxxas.com{item.get('href')}")
        else:
            if f"https://traxxas.com{item.get('href')}" not in item_urls_landing:
                item_urls_landing.append(f"https://traxxas.com{item.get('href')}")
        if cou > 10:
            break

    # coun = 0
    for item in item_urls_landing:
        # coun+=1
        try:
            driver.get(item)
            beautiful_landin = BeautifulSoup(driver.page_source, 'lxml')
            buy_option = beautiful_landin.select('.col-sm-12 div a')
            for em in buy_option:
                if 'models/' in em.get('href'):
                    item_urls.append(f"https://traxxas.com{em.get('href')}")
                else:
                    pass
        except:
            pass

    # csasd = 0
    # try:
    for item in item_urls:
        try:
            driver.get(item)
            item_url_for_the_bot = item
            beautiful_tra = BeautifulSoup(driver.page_source, 'lxml')
            product_parent = beautiful_tra.select_one('#three-column-content')
            product_name = f"{item.split('/')[-1].split('?')[0]} {product_parent.select_one('.search-result-sku').text}"
            print(product_name)
            product_description = product_name
            product_long_description = product_parent.select('.views-row')[0].text
            print(product_long_description)
            print(product_description)
            # try:
            price_original = product_parent.select_one('.search-result-price').text
            #
            print(price_original)
            price_discounted = product_parent.select_one('.search-result-price').text
            print(price_discounted)
            # / sites / default / files / images / 97054 - 1 - TRX4m - Defender - Action - Orange - Tan - 1221
            # _m.jpg
            for image in product_parent.select('img')[0].get('src'):
                if '.jpg' in image:
                    primary_image = f"https://traxxas.com{image.get('src')}"
                    break
                else:
                    primary_image = f"https://traxxas.com{product_parent.select('.views-row img')[0].get('src')}"
                    # break
            # if not primary_image:
            #     primary_image = f"https://traxxas.com{product_parent.select('img')[0].get('src')}"
            try:
                print(primary_image)
            except:
                primary_image = "Not Found"

            primary_vendor = 'Traxxas'
            print(primary_vendor)
            product_category = item.replace('https://traxxas.com/products/', '').split('?')[0].replace("/", '>')
            driver.get(f"{item}?t=gallery")
            images_beau = BeautifulSoup(driver.page_source, 'lxml')
            raw_product_images_url = ''
            for image_u in images_beau.select('.view-content img'):
                raw_product_images_url += f", https://traxxas.com{image_u.get('src')}"
            product_images_url = raw_product_images_url[2:]
            print(product_category)
            print(product_images_url)
            time.sleep(3)
            if beautiful_tra.select('.buynow-option-title'):
                for color in beautiful_tra.select('.buynow-option-title'):
                    new_prod_image_url = ''
                    for image_wit_color in product_images_url.split(','):
                        if color.text in image_wit_color:
                            new_prod_image_url += f', {image_wit_color}'
                    main_database[f"{product_name} {color.text}"] = {'Item #': f"{product_name} {color.text}",
                                                                     'Description': product_description,
                                                                     'Original Price': price_original,
                                                                     'Current Price': price_discounted,
                                                                     'Long Description': product_long_description,
                                                                     'Primary Image': primary_image,
                                                                     'Primary Vendor': primary_vendor,
                                                                     'Category': product_category,
                                                                     'Item Images URL': new_prod_image_url,
                                                                     "Item Url": item_url_for_the_bot,
                                                                     'Scraped time details': time.asctime()
                                                                     }
            else:
                main_database[product_name] = {'Item #': product_name,
                                               'Description': product_description,
                                               'Original Price': price_original,
                                               'Current Price': price_discounted,
                                               'Long Description': product_long_description,
                                               'Primary Image': primary_image,
                                               'Primary Vendor': primary_vendor,
                                               'Category': product_category,
                                               'Item Images URL': product_images_url,
                                               "Item Url": item_url_for_the_bot,
                                               'Scraped time details': time.asctime()

                                               }

        # print(item_urls)
        except:
            pass

    counter_page = 0
    while True:
        counter_page += 1
        try:
            driver.get(
                f'https://traxxas.com/products/search?keyword=&sort_by=search_api_relevance&sort_order=DESC&items_per_page=100&page={counter_page}')
            if 'No results' in driver.page_source:
                break
            else:
                pass
            refrom = BeautifulSoup(driver.page_source, 'lxml')
            pro_on_pages = refrom.select('.views-row a')
            all_urls_traxx = []
            for ur in pro_on_pages:
                if 'latrax' not in ur.get('href') and 'products' in ur.get('href'):
                    all_urls_traxx.append(f"https://traxxas.com{ur.get('href')}")
                else:
                    pass
            for item in all_urls_traxx:
                driver.get(item)
                item_url_for_the_bot = item
                beautiful_tra = BeautifulSoup(driver.page_source, 'lxml')
                product_parent = beautiful_tra.select_one('#three-column-content')
                product_name = f"{item.split('/')[-1].split('?')[0]} {product_parent.select_one('.search-result-sku').text}"
                print(product_name)
                product_description = product_name
                product_long_description = product_parent.select('.views-row')[0].text
                print(product_long_description)
                print(product_description)
                # try:
                price_original = product_parent.select_one('.search-result-price').text
                #
                print(price_original)
                price_discounted = product_parent.select_one('.search-result-price').text
                print(price_discounted)
                # / sites / default / files / images / 97054 - 1 - TRX4m - Defender - Action - Orange - Tan - 1221
                # _m.jpg
                for image in product_parent.select('img')[0].get('src'):
                    if '.jpg' in image:
                        primary_image = f"https://traxxas.com{image.get('src')}"
                        break
                    else:
                        primary_image = f"https://traxxas.com{product_parent.select('.views-row img')[0].get('src')}"
                # if not primary_image:
                #     primary_image = f"https://traxxas.com{product_parent.select('img')[0].get('src')}"
                try:
                    print(primary_image)
                except:
                    primary_image = "Not Found"

                primary_vendor = 'Traxxas'
                print(primary_vendor)
                product_category = item.replace('https://traxxas.com/products/', '').split('?')[0].replace("/", '>')
                driver.get(f"{item}?t=gallery")
                images_beau = BeautifulSoup(driver.page_source, 'lxml')
                raw_product_images_url = ''
                for image_u in images_beau.select('.view-content img'):
                    raw_product_images_url += f", https://traxxas.com{image_u.get('src')}"
                product_images_url = raw_product_images_url[2:]
                print(product_category)
                print(product_images_url)
                time.sleep(3)
                if beautiful_tra.select('.buynow-option-title'):
                    for color in beautiful_tra.select('.buynow-option-title'):
                        new_prod_image_url = ''
                        for image_wit_color in product_images_url.split(','):
                            if color.text in image_wit_color:
                                new_prod_image_url += f', {image_wit_color}'
                        main_database[f"{product_name} {color.text}"] = {'Item #': f"{product_name} {color.text}",
                                                                         'Description': product_description,
                                                                         'Original Price': price_original,
                                                                         'Current Price': price_discounted,
                                                                         'Long Description': product_long_description,
                                                                         'Primary Image': primary_image,
                                                                         'Primary Vendor': primary_vendor,
                                                                         'Category': product_category,
                                                                         'Item Images URL': new_prod_image_url,
                                                                         "Item Url": item_url_for_the_bot,
                                                                         'Scraped time details': time.asctime()
                                                                         }
                else:
                    main_database[product_name] = {'Item #': product_name,
                                                   'Description': product_description,
                                                   'Original Price': price_original,
                                                   'Current Price': price_discounted,
                                                   'Long Description': product_long_description,
                                                   'Primary Image': primary_image,
                                                   'Primary Vendor': primary_vendor,
                                                   'Category': product_category,
                                                   'Item Images URL': product_images_url,
                                                   "Item Url": item_url_for_the_bot,
                                                   'Scraped time details': time.asctime()

                                                   }
        except:
            pass
    driver.get('https://traxxas.com/products/parts/batteries-chargers')
    all_battery = []
    beautiful_tra_battery = BeautifulSoup(driver.page_source, 'lxml')
    for item in beautiful_tra_battery.select('.wrapper a'):
        if 'cart' not in item.get('href') and 'products' in item.get('href'):
            all_battery.append(f"https://traxxas.com{item.get('href')}")

    for item in all_battery:
        try:
            driver.get(item)
            item_url_for_the_bot = item
            beautiful_tra = BeautifulSoup(driver.page_source, 'lxml')
            product_parent = beautiful_tra.select_one('#three-column-content')
            product_name = f"{item.split('/')[-1].split('?')[0]} {product_parent.select_one('.search-result-sku').text}"
            print(product_name)
            product_description = product_name
            product_long_description = product_parent.select('.views-row')[0].text
            print(product_long_description)
            print(product_description)
            # try:
            price_original = product_parent.select_one('.search-result-price').text
            #
            print(price_original)
            price_discounted = product_parent.select_one('.search-result-price').text
            print(price_discounted)
            # / sites / default / files / images / 97054 - 1 - TRX4m - Defender - Action - Orange - Tan - 1221
            # _m.jpg
            for image in product_parent.select('img')[0].get('src'):
                if '.jpg' in image:
                    primary_image = f"https://traxxas.com{image.get('src')}"
                    break
                else:
                    primary_image = f"https://traxxas.com{product_parent.select('.views-row img')[0].get('src')}"
            # if not primary_image:
            #     primary_image = f"https://traxxas.com{product_parent.select('img')[0].get('src')}"
            try:
                print(primary_image)
            except:
                primary_image = "Not Found"

            primary_vendor = 'Traxxas'
            print(primary_vendor)
            product_category = item.replace('https://traxxas.com/products/', '').split('?')[0].replace("/", '>')
            driver.get(f"{item}?t=gallery")
            images_beau = BeautifulSoup(driver.page_source, 'lxml')
            raw_product_images_url = ''
            for image_u in images_beau.select('.view-content img'):
                raw_product_images_url += f", https://traxxas.com{image_u.get('src')}"
            product_images_url = raw_product_images_url[2:]
            print(product_category)
            print(product_images_url)
            time.sleep(3)
            main_database[product_name] = {'Item #': product_name,
                                           'Description': product_description,
                                           'Original Price': price_original,
                                           'Current Price': price_discounted,
                                           'Long Description': product_long_description,
                                           'Primary Image': primary_image,
                                           'Primary Vendor': primary_vendor,
                                           'Category': product_category,
                                           'Item Images URL': product_images_url,
                                           "Item Url": item_url_for_the_bot,
                                           'Scraped time details': time.asctime()

                                           }
        except:
            pass












    res_po_ = requests.get('https://www.hobbyrecreationproducts.com/pages/other-brands')
    beas_resp = BeautifulSoup(res_po_.text, 'lxml')
    print(res_po_)
    hobbU_brabds = []
    pri = (beas_resp.select('.section .block-grid li a'))
    for item in pri:

        if item.get('href'):
            hobbU_brabds.append(f"https://www.hobbyrecreationproducts.com{item.get('href')}")
        # break
    print(hobbU_brabds)
    for ite in hobbU_brabds:
        # (ite)
        counter = 0
        all_items_links = []
        while True:
            try:
                counter += 1
                print(f'https://www.hobbyrecreationproducts.com/pages/search-results-page?collection={ite.replace("https://www.hobbyrecreationproducts.com/collections/", "").replace(" ", "")}&tab=products&page={counter}')
                # res = requests.get(f'https://www.hobbyrecreationproducts.com/pages/search-results-page?collection={ite.replace("https://www.hobbyrecreationproducts.com/collections/", "").replace(" ","")}&tab=products&page={counter}', timeout=6)
                # print(res.text)

                driver.get(
                    f'https://www.hobbyrecreationproducts.com/pages/search-results-page?collection={ite.replace("https://www.hobbyrecreationproducts.com/collections/", "").replace(" ", "")}&tab=products&page={counter}')

                beauti = BeautifulSoup(driver.page_source, 'lxml')
                if 'Nothing found' not in beauti.text:
                    prod_items = beauti.select('.snize-product .snize-view-link')
                    for item in prod_items:
                        all_items_links.append(f"https://www.hobbyrecreationproducts.com{item.get('href')}")
                    # break
                else:
                    break
                print(all_items_links)
            except:
                pass
        for url in all_items_links:
            try:
                rewer = requests.get(url)
                item_url_for_the_bot = url
                product_parent = BeautifulSoup(rewer.text, 'lxml').select('#main .clearfix')[0]
                # driver.get(pro_url)
                # beautiful_amain_pro_page = BeautifulSoup(driver.page_source, 'lxml')
                # beautiful_amain_pro_page.select()
                product_name = product_parent.select_one('.shopify-product-form .sku-info').text.replace('\n', ' ').replace('  ', '')
                print(product_name)
                product_description = product_parent.select_one('.product-block .page-title').text.replace('\n', ' ').replace('  ', '')
                product_long_description = product_parent.select('.product-description')[0].text.replace('\n', ' ').replace('  ', '')
                print(product_long_description)
                print(product_description)
                try:
                    price_original = product_parent.select('.price-money')[1].text.replace('\n', ' ').replace('  ', '')
                except:
                    price_original = product_parent.select('.price-money')[0].text.replace('\n', ' ').replace('  ', '')
                print(price_original)
                price_discounted = product_parent.select('.price-money')[0].text.replace('\n', ' ').replace('  ', '')
                print(price_discounted)
                primary_image = f"https:{product_parent.select_one('.feature-row__image').get('src')}".replace('\n', ' ').replace('  ', '')
                print(primary_image)
                primary_vendor = product_description.split("-")[0].replace('\n', ' ').replace('  ', '')
                print(primary_vendor)
                product_category = "Not found"
                raw_product_images_url = ''
                for image_u in product_parent.select('.product-images img')[1:]:
                    raw_product_images_url += f", https:{image_u.get('src')}"
                product_images_url = raw_product_images_url[2:]
                print(product_category)
                print(product_images_url)
                time.sleep(3)
                main_database[product_name] = {'Item #': product_name,
                                               'Description': product_description,
                                               'Original Price': price_original,
                                               'Current Price': price_discounted,
                                               'Long Description': product_long_description,
                                               'Primary Image': primary_image,
                                               'Primary Vendor': primary_vendor,
                                               'Category': product_category,
                                               'Item Images URL': product_images_url,
                                               "Item Url": item_url_for_the_bot,
                                               'Scraped time details': time.asctime()

                                               }
            except:
                pass    # driver.get()


    hot_all_pages = []
    rawe = BeautifulSoup(requests.get('https://hot-racing.com/').text, 'lxml')
    # erasd = requests.get('https://hot-racing.com/?c=606_Associated_TC-6_Electric_Sedan').text
    for bran in (rawe.select('.menu a')):
        if 'https' in bran.get('href'):
            hot_all_pages.append(str(bran.get('href')))
        # print('firdt ')

    for item in hot_all_pages:
        # try:
        all_pro_url = []
        bea_hot = BeautifulSoup(requests.get(item).text, 'lxml')
        pro_on_pages = bea_hot.select('.callout a')
        print(pro_on_pages)
        for itc in pro_on_pages:
            if "https://hot-racing.com/" in itc.get('href') and itc.get('href') not in all_pro_url:
                all_pro_url.append(itc.get('href'))
        print(pro_on_pages)
        for tic in all_pro_url:
            print(tic)
            try:
                # try:
                # rewer = requests.get(url)
                # product_parent = BeautifulSoup(rewer.text, 'lxml').select('#main .clearfix')[0]
                # try:

                item_url_for_the_bot = tic
                bea_hot_pro = BeautifulSoup(requests.get(tic).text, 'lxml')
                # try:
                product_parent = bea_hot_pro.select('.comp-lwaq3dfy')[0]
                # except:
                # print(tic)
                # driver.get(pro_url)
                # beautiful_amain_pro_page = BeautifulSoup(driver.page_source, 'lxml')
                # beautiful_amain_pro_page.select()
                product_name = product_parent.select('.HcOXKn p .wixui-rich-text__text')[1].text
                # print(product_name[1].text)
                product_description = product_parent.select_one('.font_2').text
                product_long_description = product_parent.select('.mKHBQH')[0].text
                print(product_name)
                print(product_long_description)
                print(product_description)
                # try:
                #     price_original = product_parent.select('#comp-lwaq3dfy_r_comp-kq0trxmy_r_comp-kq0t04mf .font_8')[1].text
                # except:
                price_original = product_parent.select('#comp-lwaq3dfy_r_comp-kq0trxmy_r_comp-kq0t04mf .font_8')[0].text
                print(price_original)
                price_discounted = price_original  # product_parent.select('.font_8')[0].text
                print(price_discounted)
                if "https" not in product_parent.select_one('picture .gallery-item-visible').get('src'):
                    primary_image = f"https{product_parent.select_one('picture .gallery-item-visible').get('src')}"
                else:
                    primary_image = f"{product_parent.select_one('picture .gallery-item-visible').get('src')}"
                print(primary_image)
                primary_vendor = 'hot-racing'
                print(primary_vendor)
                product_category = product_name
                raw_product_images_url = ''
                for image_u in product_parent.select('.thumbnailItem'):
                    ra_i = image_u.get('style').split('background-image:url(')[-1].split(')')[0]
                    raw_product_images_url += f", {ra_i}"
                product_images_url = raw_product_images_url[2:]
                print('PRO CAT', product_category)
                print(product_images_url)
                print(item_url_for_the_bot)
                time.sleep(1)
                main_database[product_name] = {'Item #': product_name,
                                               'Description': product_description,
                                               'Original Price': price_original,
                                               'Current Price': price_discounted,
                                               'Long Description': product_long_description,
                                               'Primary Image': primary_image,
                                               'Primary Vendor': primary_vendor,
                                               'Category': product_category,
                                               'Item Images URL': product_images_url,
                                               "Item Url": item_url_for_the_bot,
                                               'Scraped time details': time.asctime()

                                               }
            except:
                print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE', tic)
                # except:
                #     pass
        # except:
        #     pass
        print(all_pro_url)
    # print(hobbU_brabds)
elif user_input == 'amain':
    res = requests.get('https://www.amainhobbies.com/brands')
    all_product_urls = []
    print(len(BeautifulSoup(res.text, 'lxml').select('.branditem')))
    for item in (BeautifulSoup(res.text, 'lxml').select('.branditem')):
        try:
            all_product_urls.append(f'https://www.amainhobbies.com{item.select("a")[0].get("href")}')
        except:
            pass
    # driver = Chrome(service=Service(ChromeDriverManager().install()))

    for item in all_product_urls:
        try:
            # print('sdf')
            product_urls = []
            counter = 0
            while True:
                counter += 1
                print(f'{item}?p={counter}'.replace(' ', ''))
                response_of_brand_p = requests.get(f'{item}?p={counter}'.replace(' ', '')).text
                # print(response_of_brand_p)
                beautiful_brands = BeautifulSoup(response_of_brand_p, 'lxml')
                # print(beautiful_brands)
                # time.sleep(20)
                all_item_on_a_page = beautiful_brands.select('.product-image')
                for prod in all_item_on_a_page:
                    product_urls.append(prod.get('data-url'))
                if 'class="next"' in beautiful_brands.text:
                    pass
                else:
                    # print('brea')
                    break
            # print(product_urls)
            for url_of_p in product_urls:
                try:
                    driver.get(url_of_p)
                    time.sleep(3)
                    beautiful = BeautifulSoup(driver.page_source, 'lxml')
                    product_parent = beautiful.select('#product-info')[0]
                    # print(product_parent)
                    # time.sleep(40)
                    item_url_for_the_bot = url_of_p
                    product_name = product_parent.select_one('.sku').text
                    print(product_name)
                    product_description = product_parent.select_one('.productname').text.replace("\n", ' ')
                    product_long_description = beautiful.select('.tabs .tabcontent p')[0].text
                    print(product_long_description)
                    print(product_description)
                    try:
                        price_original = product_parent.select_one('.price s').text
                    except:
                        price_original = product_parent.select_one('.theprice td').text
                    print(price_original)
                    price_discounted = product_parent.select_one('.theprice td').text
                    print(price_discounted)
                    primary_image = product_parent.select('.mainphoto img')[0].get('src')
                    print(primary_image)
                    primary_vendor = product_parent.select('div .brandname span')[0].text
                    print(primary_vendor)
                    product_category = product_parent.select('.breadcrumb')[0].text.replace('\n', '')
                    raw_product_images_url = ''
                    for image_u in product_parent.select('.carousel img'):
                        raw_product_images_url += f", {image_u.get('src').replace('width=100', 'width=500')}"
                    product_images_url = raw_product_images_url[2:]
                    print(product_category)
                    print(product_images_url)
                    time.sleep(3)
                    main_database[product_name] = {'Item #': product_name,
                                                   'Description': product_description,
                                                   'Original Price': price_original,
                                                   'Current Price': price_discounted,
                                                   'Long Description': product_long_description,
                                                   'Primary Image': primary_image,
                                                   'Primary Vendor': primary_vendor,
                                                   'Category': product_category,
                                                   'Item Images URL': product_images_url,
                                                   "Item Url": item_url_for_the_bot,
                                                   'Scraped time details': time.asctime()
                                                   }
                    print(main_database, '-----------------------------------------------------------------------')
                except:
                    # pass
                    data_to_create_csv = {'Item #': [],
                                          'Description': [],
                                          'Original Price': [],
                                          'Current Price': [],
                                          'Long Description': [],
                                          'Primary Image': [],
                                          'Primary Vendor': [],
                                          'Category': [],
                                          'Item Images URL': [],
                                          "Item Url": []
                                          }

                    for ite in main_database:
                        for main in main_database[ite]:
                            data_to_create_csv[main].append(main_database[ite][main])

                    data_frame_pandas = pandas.DataFrame(data_to_create_csv)
                    data_frame_pandas.to_csv('scraped_data.csv')

        except:
            pass

elif user_input == 'horizon':
    ree = requests.get('https://www.horizonhobby.com/brands/')
    # print(ree.text)

    links_of_brands = []

    beautiful_horizon = BeautifulSoup(ree.text, 'lxml')
    for item in beautiful_horizon.select('.card'):
        try:
            links_of_brands.append(item.select('a')[0].get('href').split('?')[0])
        except:
            pass


    # print(links_of_brands)

    for li in links_of_brands:
        try:
            counter_page = 0
            product_urls_hori = []
            while True:
                # if

                respoof_hori = requests.get(
                    f'{li}?prefn1=discontinued&prefv1=false&start={counter_page}&sz=100&return=true').text
                beautiful_horizon_prod = BeautifulSoup(respoof_hori, 'lxml')
                counter_page += 100
                if 'class="product-tile"' in respoof_hori:
                    pass
                else:
                    break
                raw_pro = beautiful_horizon_prod.select('.product-tile-img-container')
                for raw in raw_pro:
                    product_urls_hori.append(f'https://www.horizonhobby.com{raw.get("href")}')
                print(product_urls_hori)
            for prod in product_urls_hori:
                try:
                    driver.get(prod)
                    item_url_for_the_bot = [prod]
                    time.sleep(3)
                    beautiful = BeautifulSoup(driver.page_source, 'lxml')
                    product_parent = beautiful.select('.product-wrapper-a')[0]
                    # print(product_parent)
                    # time.sleep(40)
                    product_name = product_parent.select_one('.product-id').text
                    print(product_name)
                    if 'class="intro-block' not in driver.page_source:
                        product_description = product_parent.select_one('.product-name').text.replace('\n', '').replace('                                ', '')
                    else:
                        product_description = beautiful.select_one('.intro-block').text.replace('\n', '').replace(
                            '                                ', '')

                    if 'long-desc-content' not in driver.page_source:
                        product_long_description = product_description.replace('\n', '').replace(
                            '                                ', '')
                    else:
                        product_long_description = beautiful.select_one('.long-desc-content').select_one('p').text.replace(
                            '\n', '').replace('                                ', '')
                    print(product_long_description)
                    print(product_description)

                    try:
                        price_original = product_parent.select_one('.callout').text.replace('Was ', '').split('.')[
                            0].replace('\n', '').replace(' ', '')
                    except:
                        price_original = product_parent.select_one('.value').text.replace('\n', '').replace(' ', '')
                    print(price_original)
                    price_discounted = product_parent.select_one('.value').text.replace('\n', '').replace(' ', '')
                    print(price_discounted)
                    primary_image = product_parent.select('.slick-slide img')[0].get('src').replace('\n', '').replace(
                        '                                ', '')
                    print(primary_image)
                    primary_vendor = product_parent.select('.product-number .name-wrapper span')[0].text.replace('-',
                                                                                                                 '').replace(
                        '\n', '').replace('                                ', '')
                    print(primary_vendor)
                    product_category = product_parent.select('.breadcrumb')[0].text.replace('\n', '').replace(
                        '                                                    ', '>').replace('                            ',
                                                                                             '')
                    raw_product_images_url = ''
                    for image_u in product_parent.select('.slick-slide img')[1:]:
                        if "None" not in str(image_u.get('src')):
                            raw_product_images_url += f", {image_u.get('src')}"
                    product_images_url = raw_product_images_url[2:]
                    print(product_category)
                    print(product_images_url)
                    time.sleep(3)
                    main_database[product_name] = {'Item #': product_name,
                                                   'Description': product_description,
                                                   'Original Price': price_original,
                                                   'Current Price': price_discounted,
                                                   'Long Description': product_long_description,
                                                   'Primary Image': primary_image,
                                                   'Primary Vendor': primary_vendor,
                                                   'Category': product_category,
                                                   'Item Images URL': product_images_url,
                                                   "Item Url": item_url_for_the_bot,
                                                   'Scraped time details': time.asctime()
                                                   }
                except:
                    pass
        except:
            pass

elif user_input =='traxxas':

    list_of_goto = ["https://traxxas.com/products/showroom", 'https://traxxas.com/products/parts/batteries-chargers']
    # driver.get().text
    # time.sleep(10)
    # print(driver.page_source)
    # for it in list_of_goto:
    driver.get(list_of_goto[0])
    beautiful_la = BeautifulSoup(driver.page_source, 'lxml')
    all_models = beautiful_la.select('.views-view-grid tbody tr td a')
    item_urls = []
    item_urls_landing = []
    cou = 0
    for item in all_models:
        try:
            cou += 1
            if 'landing' not in item.get('href') and f"https://traxxas.com{item.get('href')}" not in item_urls:
                item_urls.append(f"https://traxxas.com{item.get('href')}")
            else:
                if f"https://traxxas.com{item.get('href')}" not in item_urls_landing:
                    item_urls_landing.append(f"https://traxxas.com{item.get('href')}")
        except:
            pass

    # coun = 0
    for item in item_urls_landing:
        # coun+=1
        try:
            driver.get(item)
            beautiful_landin = BeautifulSoup(driver.page_source, 'lxml')
            buy_option = beautiful_landin.select('.col-sm-12 div a')
            for em in buy_option:
                if 'models/' in em.get('href'):
                    item_urls.append(f"https://traxxas.com{em.get('href')}")
                else:
                    pass
        except:
            pass
    print(item_urls)
    # csasd = 0
    # try:
    for item in item_urls:
        try:
            driver.get(item)
            item_url_for_the_bot = item
            beautiful_tra = BeautifulSoup(driver.page_source, 'lxml')
            product_parent = beautiful_tra.select_one('#three-column-content')
            product_name = f"{item.split('/')[-1].split('?')[0]} {product_parent.select_one('.search-result-sku').text}"
            print(product_name)
            product_description = product_name
            product_long_description = product_parent.select('.views-row')[0].text
            print(product_long_description)
            print(product_description)
            # try:
            price_original = product_parent.select_one('.search-result-price').text
            #
            print(price_original)
            price_discounted = product_parent.select_one('.search-result-price').text
            print(price_discounted)
            # / sites / default / files / images / 97054 - 1 - TRX4m - Defender - Action - Orange - Tan - 1221
            # _m.jpg
            for image in product_parent.select('img')[0].get('src'):
                if '.jpg' in image:
                    primary_image = f"https://traxxas.com{image.get('src')}"
                    break
                else:
                    primary_image = f"https://traxxas.com{product_parent.select('.views-row img')[0].get('src')}"
                    # break
            # if not primary_image:
            #     primary_image = f"https://traxxas.com{product_parent.select('img')[0].get('src')}"
            try:
                print(primary_image)
            except:
                primary_image = "Not Found"

            primary_vendor = 'Traxxas'
            print(primary_vendor)
            product_category = item.replace('https://traxxas.com/products/', '').split('?')[0].replace("/", '>')
            driver.get(f"{item}?t=gallery")
            images_beau = BeautifulSoup(driver.page_source, 'lxml')
            raw_product_images_url = ''
            for image_u in images_beau.select('.view-content img'):
                raw_product_images_url += f", https://traxxas.com{image_u.get('src')}"
            product_images_url = raw_product_images_url[2:]
            print(product_category)
            print(product_images_url)
            if beautiful_tra.select('.buynow-option-title'):
                for color in beautiful_tra.select('.buynow-option-title'):
                    new_prod_image_url = ''
                    for image_wit_color in product_images_url.split(','):
                        if color.text in image_wit_color:
                            new_prod_image_url += f', {image_wit_color}'
                    main_database[f"{product_name} {color.text}"] = {'Item #': f"{product_name} {color.text}",
                                                                     'Description': product_description,
                                                                     'Original Price': price_original,
                                                                     'Current Price': price_discounted,
                                                                     'Long Description': product_long_description,
                                                                     'Primary Image': primary_image,
                                                                     'Primary Vendor': primary_vendor,
                                                                     'Category': product_category,
                                                                     'Item Images URL': new_prod_image_url,
                                                                     "Item Url": item_url_for_the_bot,
                                                                     'Scraped time details': time.asctime()
                                                                     }
            else:
                main_database[product_name] = {'Item #': product_name,
                                               'Description': product_description,
                                               'Original Price': price_original,
                                               'Current Price': price_discounted,
                                               'Long Description': product_long_description,
                                               'Primary Image': primary_image,
                                               'Primary Vendor': primary_vendor,
                                               'Category': product_category,
                                               'Item Images URL': product_images_url,
                                               "Item Url": item_url_for_the_bot,
                                               'Scraped time details': time.asctime()

                                               }
            time.sleep(20)

        except:
            pass
        print(main_database)

    counter_page = 0
    while True:
        try:
            driver.get(
                f'https://traxxas.com/products/search?keyword=&sort_by=search_api_relevance&sort_order=DESC&items_per_page=100&page={counter_page}')
            if 'No results' in driver.page_source:
                break
            else:
                pass
            refrom = BeautifulSoup(driver.page_source, 'lxml')
            pro_on_pages = refrom.select('.views-row a')
            all_urls_traxx = []
            for ur in pro_on_pages:
                if 'latrax' not in ur.get('href') and 'products' in ur.get('href'):
                    all_urls_traxx.append(f"https://traxxas.com{ur.get('href')}")
                else:
                    pass
            for item in all_urls_traxx:
                try:
                    driver.get(item)
                    item_url_for_the_bot = item
                    beautiful_tra = BeautifulSoup(driver.page_source, 'lxml')
                    product_parent = beautiful_tra.select_one('#three-column-content')
                    product_name = f"{item.split('/')[-1].split('?')[0]} {product_parent.select_one('.search-result-sku').text}"
                    print(product_name)
                    product_description = product_name
                    product_long_description = product_parent.select('.views-row')[0].text
                    print(product_long_description)
                    print(product_description)
                    # try:
                    price_original = product_parent.select_one('.search-result-price').text
                    #
                    print(price_original)
                    price_discounted = product_parent.select_one('.search-result-price').text
                    print(price_discounted)
                    # / sites / default / files / images / 97054 - 1 - TRX4m - Defender - Action - Orange - Tan - 1221
                    # _m.jpg
                    for image in product_parent.select('img')[0].get('src'):
                        if '.jpg' in image:
                            primary_image = f"https://traxxas.com{image.get('src')}"
                            break
                        else:
                            primary_image = f"https://traxxas.com{product_parent.select('.views-row img')[0].get('src')}"
                    # if not primary_image:
                    #     primary_image = f"https://traxxas.com{product_parent.select('img')[0].get('src')}"
                    try:
                        print(primary_image)
                    except:
                        primary_image = "Not Found"

                    primary_vendor = 'Traxxas'
                    print(primary_vendor)
                    product_category = item.replace('https://traxxas.com/products/', '').split('?')[0].replace("/", '>')
                    driver.get(f"{item}?t=gallery")
                    images_beau = BeautifulSoup(driver.page_source, 'lxml')
                    raw_product_images_url = ''
                    for image_u in images_beau.select('.view-content img'):
                        raw_product_images_url += f", https://traxxas.com{image_u.get('src')}"
                    product_images_url = raw_product_images_url[2:]
                    print(product_category)
                    print(product_images_url)
                    time.sleep(3)
                    if beautiful_tra.select('.buynow-option-title'):
                        for color in beautiful_tra.select('.buynow-option-title'):
                            new_prod_image_url = ''
                            for image_wit_color in product_images_url.split(','):
                                if color.text in image_wit_color:
                                    new_prod_image_url += f', {image_wit_color}'
                            main_database[f"{product_name} {color.text}"] = {'Item #': f"{product_name} {color.text}",
                                                                             'Description': product_description,
                                                                             'Original Price': price_original,
                                                                             'Current Price': price_discounted,
                                                                             'Long Description': product_long_description,
                                                                             'Primary Image': primary_image,
                                                                             'Primary Vendor': primary_vendor,
                                                                             'Category': product_category,
                                                                             'Item Images URL': new_prod_image_url,
                                                                             "Item Url": item_url_for_the_bot,
                                                                             'Scraped time details': time.asctime()
                                                                             }
                    else:
                        main_database[product_name] = {'Item #': product_name,
                                                       'Description': product_description,
                                                       'Original Price': price_original,
                                                       'Current Price': price_discounted,
                                                       'Long Description': product_long_description,
                                                       'Primary Image': primary_image,
                                                       'Primary Vendor': primary_vendor,
                                                       'Category': product_category,
                                                       'Item Images URL': product_images_url,
                                                       "Item Url": item_url_for_the_bot,
                                                       'Scraped time details': time.asctime()
                                                       }
                except:
                    pass

        except:
            pass
        counter_page += 1

    driver.get('https://traxxas.com/products/parts/batteries-chargers')
    all_battery = []
    beautiful_tra_battery = BeautifulSoup(driver.page_source, 'lxml')
    for item in beautiful_tra_battery.select('.wrapper a'):
        if 'cart' not in item.get('href') and 'products' in item.get('href'):
            all_battery.append(f"https://traxxas.com{item.get('href')}")

    for item in all_battery:
        try:
            driver.get(item)
            item_url_for_the_bot = item
            beautiful_tra = BeautifulSoup(driver.page_source, 'lxml')
            product_parent = beautiful_tra.select_one('#three-column-content')
            product_name = f"{item.split('/')[-1].split('?')[0]} {product_parent.select_one('.search-result-sku').text}"
            print(product_name)
            product_description = product_name
            product_long_description = product_parent.select('.views-row')[0].text
            print(product_long_description)
            print(product_description)
            # try:
            price_original = product_parent.select_one('.search-result-price').text
            #
            print(price_original)
            price_discounted = product_parent.select_one('.search-result-price').text
            print(price_discounted)
            # / sites / default / files / images / 97054 - 1 - TRX4m - Defender - Action - Orange - Tan - 1221
            # _m.jpg
            for image in product_parent.select('img')[0].get('src'):
                if '.jpg' in image:
                    primary_image = f"https://traxxas.com{image.get('src')}"
                    break
                else:
                    primary_image = f"https://traxxas.com{product_parent.select('.views-row img')[0].get('src')}"
            # if not primary_image:
            #     primary_image = f"https://traxxas.com{product_parent.select('img')[0].get('src')}"
            try:
                print(primary_image)
            except:
                primary_image = "Not Found"

            primary_vendor = 'Traxxas'
            print(primary_vendor)
            product_category = item.replace('https://traxxas.com/products/', '').split('?')[0].replace("/", '>')
            driver.get(f"{item}?t=gallery")
            images_beau = BeautifulSoup(driver.page_source, 'lxml')
            raw_product_images_url = ''
            for image_u in images_beau.select('.view-content img'):
                raw_product_images_url += f", https://traxxas.com{image_u.get('src')}"
            product_images_url = raw_product_images_url[2:]
            print(product_category)
            print(product_images_url)
            time.sleep(3)
            main_database[product_name] = {'Item #': product_name,
                                           'Description': product_description,
                                           'Original Price': price_original,
                                           'Current Price': price_discounted,
                                           'Long Description': product_long_description,
                                           'Primary Image': primary_image,
                                           'Primary Vendor': primary_vendor,
                                           'Category': product_category,
                                           'Item Images URL': product_images_url,
                                           "Item Url": item_url_for_the_bot,
                                           'Scraped time details': time.asctime()

                                           }
        except:
            pass

elif user_input == 'hotracing':
    # driver.get('https://hot-racing.com/')
    hot_all_pages = []
    rawe = BeautifulSoup(requests.get('https://hot-racing.com/').text, 'lxml')
    # erasd = requests.get('https://hot-racing.com/?c=606_Associated_TC-6_Electric_Sedan').text
    for bran in (rawe.select('.menu a')):
        if 'https' in bran.get('href'):
            hot_all_pages.append(str(bran.get('href')))
        # print('firdt ')

    for item in hot_all_pages:
        # try:
        all_pro_url = []
        bea_hot = BeautifulSoup(requests.get(item).text, 'lxml')
        pro_on_pages = bea_hot.select('.callout a')
        print(pro_on_pages)
        for itc in pro_on_pages:
            if "https://hot-racing.com/" in itc.get('href') and itc.get('href') not in all_pro_url:
                all_pro_url.append(itc.get('href'))
        print(pro_on_pages)
        for tic in all_pro_url:
            print(tic)
            try:
            # try:
            # rewer = requests.get(url)
            # product_parent = BeautifulSoup(rewer.text, 'lxml').select('#main .clearfix')[0]
            # try:

                item_url_for_the_bot = tic
                bea_hot_pro = BeautifulSoup(requests.get(tic).text, 'lxml')
                # try:
                product_parent = bea_hot_pro.select('.comp-lwaq3dfy')[0]
                # except:
                    # print(tic)
                # driver.get(pro_url)
                # beautiful_amain_pro_page = BeautifulSoup(driver.page_source, 'lxml')
                # beautiful_amain_pro_page.select()
                product_name = product_parent.select('.HcOXKn p .wixui-rich-text__text')[1].text
                # print(product_name[1].text)
                product_description = product_parent.select_one('.font_2').text
                product_long_description = product_parent.select('.mKHBQH')[0].text
                print(product_name)
                print(product_long_description)
                print(product_description)
                # try:
                #     price_original = product_parent.select('#comp-lwaq3dfy_r_comp-kq0trxmy_r_comp-kq0t04mf .font_8')[1].text
                # except:
                price_original = product_parent.select('#comp-lwaq3dfy_r_comp-kq0trxmy_r_comp-kq0t04mf .font_8')[0].text
                print(price_original)
                price_discounted = price_original#product_parent.select('.font_8')[0].text
                print(price_discounted)
                if "https" not in product_parent.select_one('picture .gallery-item-visible').get('src'):
                    primary_image = f"https{product_parent.select_one('picture .gallery-item-visible').get('src')}"
                else:
                    primary_image = f"{product_parent.select_one('picture .gallery-item-visible').get('src')}"
                print(primary_image)
                primary_vendor = 'hot-racing'
                print(primary_vendor)
                product_category = product_name
                raw_product_images_url = ''
                for image_u in product_parent.select('.thumbnailItem'):
                    ra_i = image_u.get('style').split('background-image:url(')[-1].split(')')[0]
                    raw_product_images_url += f", {ra_i}"
                product_images_url = raw_product_images_url[2:]
                print('PRO CAT', product_category)
                print(product_images_url)
                print(item_url_for_the_bot)
                time.sleep(1)
                main_database[product_name] = {'Item #': product_name,
                                               'Description': product_description,
                                               'Original Price': price_original,
                                               'Current Price': price_discounted,
                                               'Long Description': product_long_description,
                                               'Primary Image': primary_image,
                                               'Primary Vendor': primary_vendor,
                                               'Category': product_category,
                                               'Item Images URL': product_images_url,
                                               "Item Url": item_url_for_the_bot,
                                               'Scraped time details': time.asctime()

                                               }
            except:
                print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE', tic)
                    # except:
                #     pass
        # except:
        #     pass
        print(all_pro_url)
elif user_input == 'hobbyrecreation':

    res_po_ = requests.get('https://www.hobbyrecreationproducts.com/pages/other-brands')
    beas_resp = BeautifulSoup(res_po_.text, 'lxml')
    print(res_po_)
    hobbU_brabds = []
    pri = (beas_resp.select('.section .block-grid li a'))
    for item in pri:

        if item.get('href'):
            hobbU_brabds.append(f"https://www.hobbyrecreationproducts.com{item.get('href')}")
        # break
    print(hobbU_brabds)
    for ite in hobbU_brabds:
        # (ite)
        counter = 0
        all_items_links = []
        while True:
            try:
                counter += 1
                print(f'https://www.hobbyrecreationproducts.com/pages/search-results-page?collection={ite.replace("https://www.hobbyrecreationproducts.com/collections/", "").replace(" ", "")}&tab=products&page={counter}')
                # res = requests.get(f'https://www.hobbyrecreationproducts.com/pages/search-results-page?collection={ite.replace("https://www.hobbyrecreationproducts.com/collections/", "").replace(" ","")}&tab=products&page={counter}', timeout=6)
                # print(res.text)

                driver.get(
                    f'https://www.hobbyrecreationproducts.com/pages/search-results-page?collection={ite.replace("https://www.hobbyrecreationproducts.com/collections/", "").replace(" ", "")}&tab=products&page={counter}')

                beauti = BeautifulSoup(driver.page_source, 'lxml')
                if 'Nothing found' not in beauti.text:
                    prod_items = beauti.select('.snize-product .snize-view-link')
                    for item in prod_items:
                        all_items_links.append(f"https://www.hobbyrecreationproducts.com{item.get('href')}")
                    # break
                else:
                    break
                print(all_items_links)
            except:
                pass
        for url in all_items_links:
            try:
                rewer = requests.get(url)
                item_url_for_the_bot = url
                product_parent = BeautifulSoup(rewer.text, 'lxml').select('#main .clearfix')[0]
                # driver.get(pro_url)
                # beautiful_amain_pro_page = BeautifulSoup(driver.page_source, 'lxml')
                # beautiful_amain_pro_page.select()
                product_name = product_parent.select_one('.shopify-product-form .sku-info').text.replace('\n', ' ').replace('  ', '')
                print(product_name)
                product_description = product_parent.select_one('.product-block .page-title').text.replace('\n', ' ').replace('  ', '')
                product_long_description = product_parent.select('.product-description')[0].text.replace('\n', ' ').replace('  ', '')
                print(product_long_description)
                print(product_description)
                try:
                    price_original = product_parent.select('.price-money')[1].text.replace('\n', ' ').replace('  ', '')
                except:
                    price_original = product_parent.select('.price-money')[0].text.replace('\n', ' ').replace('  ', '')
                print(price_original)
                price_discounted = product_parent.select('.price-money')[0].text.replace('\n', ' ').replace('  ', '')
                print(price_discounted)
                primary_image = f"https:{product_parent.select_one('.feature-row__image').get('src')}".replace('\n', ' ').replace('  ', '')
                print(primary_image)
                primary_vendor = product_description.split("-")[0].replace('\n', ' ').replace('  ', '')
                print(primary_vendor)
                product_category = "Not found"
                raw_product_images_url = ''
                for image_u in product_parent.select('.product-images img')[1:]:
                    raw_product_images_url += f", https:{image_u.get('src')}"
                product_images_url = raw_product_images_url[2:]
                print(product_category)
                print(product_images_url)
                time.sleep(3)
                main_database[product_name] = {'Item #': product_name,
                                               'Description': product_description,
                                               'Original Price': price_original,
                                               'Current Price': price_discounted,
                                               'Long Description': product_long_description,
                                               'Primary Image': primary_image,
                                               'Primary Vendor': primary_vendor,
                                               'Category': product_category,
                                               'Item Images URL': product_images_url,
                                               "Item Url": item_url_for_the_bot,
                                               'Scraped time details': time.asctime()

                                               }
            except:
                pass
    # driver.get()


























if not exists('scraped_data.csv'):

    data_to_create_csv = {'Item #': [],
                          'Description': [],
                          'Original Price': [],
                          'Current Price': [],
                          'Long Description': [],
                          'Primary Image': [],
                          'Primary Vendor': [],
                          'Category': [],
                          'Item Images URL': [],
                          "Item Url": [],
                          'Scraped time details':[]
                          }

    for ite in main_database:
        for main in main_database[ite]:
            data_to_create_csv[main].append(main_database[ite][main])

    data_frame_pandas = pandas.DataFrame(data_to_create_csv)
    data_frame_pandas.to_csv('scraped_data.csv')

else:
    data_sraped_already = {}
    panda = pandas.read_csv('scraped_data.csv').to_dict()


    items_name = []
    for i, it in panda['Item #'].items():
        items_name.append(it)

    descri = []
    for i, it in panda['Description'].items():
        descri.append(it)

    original_price = []
    for i, it in panda['Original Price'].items():
        original_price.append(it)

    cur_pri =[]
    for i, it in panda['Current Price'].items():
        cur_pri.append(it)

    long_des = []
    for i, it in panda['Long Description'].items():
        long_des.append(it)

    pri_img = []
    for i, it in panda['Primary Image'].items():
        pri_img.append(it)

    pri_vend = []
    for i, it in panda['Primary Vendor'].items():
        pri_vend.append(it)

    category = []
    for i, it in panda['Category'].items():
        category.append(it)

    itemimages = []
    for i, it in panda['Item Images URL'].items():
        itemimages.append(it)

    itm_url = []
    for i, it in panda['Item Url'].items():
        itm_url.append(it)

    print(itm_url)
    time_scr = []
    for i, it in panda['Scraped time details'].items():
        time_scr.append(it)
    print(time_scr)
    final_dic = {}
    for i in range(len(time_scr)):
        # print(items_name[i])
        final_dic[items_name[i]]= {'Item #': items_name[i],
         'Description': descri[i],
         'Original Price': original_price[i],
         'Current Price': cur_pri[i],
         'Long Description': long_des[i],
         'Primary Image': pri_img[i],
         'Primary Vendor': pri_vend[i],
         'Category': category[i],
         'Item Images URL': itemimages[i],
         "Item Url": itm_url[i]
         }
    for anr in main_database:
        try:
            if main_database[anr]['Item #'] == data_sraped_already[anr]['Item #'] and main_database[anr]['Description'] == data_sraped_already[anr]['Description'] and main_database[anr]['Original Price'] == data_sraped_already[anr]['Original Price']and main_database[anr]['Current Price'] == data_sraped_already[anr]['Current Price'] and main_database[anr]['Long Description'] == data_sraped_already[anr]['Long Description'] and main_database[anr]['Primary Image'] == data_sraped_already[anr]['Primary Image'] and main_database[anr]['Primary Vendor'] == data_sraped_already[anr]['Primary Vendor'] and main_database[anr]['Category'] == data_sraped_already[anr]['Category'] and main_database[anr]['Item Images URL'] == data_sraped_already[anr]['Item Images URL']:
                pass
            else:
                data_sraped_already[anr] = main_database[anr]
        except:
            data_sraped_already[anr] = main_database[anr]
    data_to_create_csv = {'Item #': [],
                          'Description': [],
                          'Original Price': [],
                          'Current Price': [],
                          'Long Description': [],
                          'Primary Image': [],
                          'Primary Vendor': [],
                          'Category': [],
                          'Item Images URL': [],
                          "Item Url": [],
                          'Scraped time details':[]
                          }

    for ite in data_sraped_already:
        for main in data_sraped_already[ite]:
            data_to_create_csv[main].append(data_sraped_already[ite][main])

    data_frame_pandas = pandas.DataFrame(data_to_create_csv)
    data_frame_pandas.to_csv(f'scraped_data.csv')
