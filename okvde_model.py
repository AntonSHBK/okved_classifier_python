import pandas as pd


class OKVEDClassifier:
    def __init__(self, okved_df: pd.DataFrame):
        # Создаем иерархию из DataFrame
        self.okved_data = self.build_hierarchy(okved_df)
        self.top_sections = self.create_top_sections()

    def build_hierarchy(self, df):
        """Построение иерархической структуры из DataFrame"""
        hierarchy = {}

        # Проходим по строкам DataFrame
        for index, row in df.iterrows():
            code = str(row['Код'])
            name = row['Название']

            # Разделяем код для определения уровня
            code_parts = code.split('.')

            if len(code_parts) == 1:
                # Основной раздел
                hierarchy[code] = {'name': name, 'sections': {}}
            elif len(code_parts) == 2:
                # Секция
                main_code = code_parts[0]
                if main_code in hierarchy:
                    hierarchy[main_code]['sections'][code] = {'name': name, 'subsections': {}}
            elif len(code_parts) == 3:
                # Подсекция
                main_code = code_parts[0]
                section_code = f"{code_parts[0]}.{code_parts[1]}"
                if main_code in hierarchy and section_code in hierarchy[main_code]['sections']:
                    hierarchy[main_code]['sections'][section_code]['subsections'][code] = name
        return hierarchy

    def create_top_sections(self):
        """Создает соответствие между буквенными разделами и цифровыми кодами"""
        top_sections = {
            'A': {'codes': ['01', '02', '03'], 'name': 'Сельское, лесное хозяйство, охота, рыболовство и рыбоводство'},
            'B': {'codes': ['05', '06', '07', '08', '09'], 'name': 'Добыча полезных ископаемых'},
            'C': {'codes': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19'], 'name': 'Обрабатывающие производства'},
            'D': {'codes': ['35'], 'name': 'Обеспечение электрической энергией, газом и паром; кондиционирование воздуха'},
            'E': {'codes': ['36', '37', '38', '39'], 'name': 'Водоснабжение; водоотведение, организация сбора и утилизации отходов, деятельность по ликвидации загрязнений'},
            'F': {'codes': ['41', '42', '43'], 'name': 'Строительство'},
            'G': {'codes': ['45', '46', '47'], 'name': 'Оптовая и розничная торговля; ремонт автотранспортных средств и мотоциклов'},
            'H': {'codes': ['49', '50', '51', '52', '53'], 'name': 'Транспортировка и хранение'},
            'I': {'codes': ['55', '56'], 'name': 'Деятельность гостиниц и предприятий общественного питания'},
            'J': {'codes': ['58', '59', '60', '61', '62', '63'], 'name': 'Деятельность в области информации и связи'},
            'K': {'codes': ['64', '65', '66'], 'name': 'Финансовая и страховая деятельность'},
            'L': {'codes': ['68'], 'name': 'Деятельность по операциям с недвижимым имуществом'},
            'M': {'codes': ['69', '70', '71', '72', '73', '74', '75'], 'name': 'Профессиональная, научная и техническая деятельность'},
            'N': {'codes': ['77', '78', '79', '80', '81', '82'], 'name': 'Деятельность административная и сопутствующие дополнительные услуги'},
            'O': {'codes': ['84'], 'name': 'Государственное управление и обеспечение военной безопасности; социальное обеспечение'},
            'P': {'codes': ['85'], 'name': 'Образование'},
            'Q': {'codes': ['86', '87', '88'], 'name': 'Деятельность в области здравоохранения и социальных услуг'},
            'R': {'codes': ['90', '91', '92', '93'], 'name': 'Деятельность в области культуры, спорта, организации досуга и развлечений'},
            'S': {'codes': ['94', '95', '96'], 'name': 'Предоставление прочих видов услуг'},
            'T': {'codes': ['97', '98'], 'name': 'Деятельность домашних хозяйств'},
            'U': {'codes': ['99'], 'name': 'Деятельность экстерриториальных организаций и органов'}
        }

        return top_sections

    def get_name_by_code(self, code):
        """Возвращает название категории по её коду"""
        code_parts = code.split('.')
        if len(code_parts) == 1:
            # Основной раздел
            return self.okved_data.get(code, {}).get('name')
        elif len(code_parts) == 2:
            # Секция
            main_code = code_parts[0]
            return self.okved_data.get(main_code, {}).get('sections', {}).get(code, {}).get('name')
        elif len(code_parts) == 3:
            # Подсекция
            main_code = code_parts[0]
            section_code = f"{code_parts[0]}.{code_parts[1]}"
            return self.okved_data.get(main_code, {}).get('sections', {}).get(section_code, {}).get('subsections', {}).get(code)

    def get_children_by_code(self, code):
        """Возвращает список всех дочерних элементов для указанного кода"""
        code_parts = code.split('.')
        children = []
        
        if len(code_parts) == 1:
            # Основной раздел
            sections = self.okved_data.get(code, {}).get('sections', {})
            for section_code, section_data in sections.items():
                children.append((section_code, section_data['name']))
                # Добавляем все подсекции
                for sub_code, sub_name in section_data.get('subsections', {}).items():
                    children.append((sub_code, sub_name))
        elif len(code_parts) == 2:
            # Секция
            main_code = code_parts[0]
            section_code = code
            subsections = self.okved_data.get(main_code, {}).get('sections', {}).get(section_code, {}).get('subsections', {})
            for sub_code, sub_name in subsections.items():
                children.append((sub_code, sub_name))

        return children

    def get_all_sections(self):
        """Возвращает список всех верхнеуровневых разделов"""
        return [(code, data['name']) for code, data in self.okved_data.items()]

    def get_all_top_sections(self):
        """Возвращает список всех буквенных разделов"""
        return [(key, self.top_sections[key]['name']) for key in self.top_sections]

    def get_children_by_top_section(self, top_section_letter):
        """Возвращает список всех категорий внутри выбранного буквенного раздела"""
        if top_section_letter in self.top_sections:
            result = []
            for code in self.top_sections[top_section_letter]['codes']:
                result.append((code, self.get_name_by_code(code)))
                # Добавляем всех "детей" раздела
                result.extend(self.get_children_by_code(code))
            return result
        else:
            return f"Раздел {top_section_letter} не найден."

    def get_full_list(self):
        """Выводит полный список всех категорий и кодов"""
        result = []
        for top_section in self.top_sections:
            result.append((top_section, self.top_sections[top_section]['name']))
            result.extend(self.get_children_by_top_section(top_section))
        return result
    
    def get_children_codes_by_code(self, code):
        """Возвращает список всех кодов дочерних элементов для указанного кода"""
        code_parts = code.split('.')
        children_codes = []

        if len(code_parts) == 1:
            # Основной раздел
            sections = self.okved_data.get(code, {}).get('sections', {})
            for section_code, section_data in sections.items():
                children_codes.append(section_code)
                # Добавляем все подсекции
                for sub_code in section_data.get('subsections', {}).keys():
                    children_codes.append(sub_code)
        elif len(code_parts) == 2:
            # Секция
            main_code = code_parts[0]
            section_code = code
            subsections = self.okved_data.get(main_code, {}).get('sections', {}).get(section_code, {}).get('subsections', {})
            for sub_code in subsections.keys():
                children_codes.append(sub_code)

        return children_codes
    
    def get_children_code_by_top_section(self, top_section_letter):
        """Возвращает список всех кодов дочерних элементов для указанного буквенного раздела"""
        children_codes = []
        
        if top_section_letter in self.top_sections:
            # Получаем все коды разделов, соответствующих данному буквенному разделу
            section_codes = self.top_sections[top_section_letter]['codes']
            
            for code in section_codes:
                # Добавляем сам код раздела
                children_codes.append(code)
                # Добавляем всех "детей" раздела (только коды)
                children_codes.extend([child_code[0] for child_code in self.get_children_by_code(code)])
        
        return children_codes