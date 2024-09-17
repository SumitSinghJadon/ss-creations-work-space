from IntelliSync_db.models import MenuMaster, ModuleMaster, ProjectMaster
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from IS_Nexus.functions import permission


def main_menu(request:WSGIRequest):
    module_code = settings.PROJECT_CODE 
    permission_list = permission.get(request, 'page_id_list')
    project = ProjectMaster.objects.get(code = module_code)
    menu_html = html = ""


    def generate_menu_html(menu_items, is_top_level=True, html=html):
        for i, item in enumerate(menu_items):
            # Design for each top-level node
            if is_top_level and item.children:
                sub_menu = generate_menu_html(item.children, is_top_level=False)
                html += f'''
                <li>
                    <details>
                        <summary class="font-semibold">
                            <div class="flex space-x-2 center-y">
                                <span class='sidebar-menu-icon'>{item.icon}</span>
                                <span class='font-semibold'>{item.name}</span>
                            </div>
                        </summary>
                        <ul>{sub_menu}</ul>
                    </details>
                </li>
                '''

            # Design for each top-level node if it is a link
            elif is_top_level and item.is_link:
                if item.id in permission_list:
                    html += f'''
                    <li>
                        <a href='{item.url}' class="flex w-full">
                            <span class='w-5'>{item.icon}</span>
                            <span class='font-semibold'>{item.name}</span>
                        </a>
                    </li>
                    '''

            # Design for all middle-level node
            elif item.children and not is_top_level:
                sub_menu = generate_menu_html(item.children, is_top_level=False)
                html += f'''
                <li>
                    <details>
                        <summary>
                            <div class="flex w-full">
                                <span>{item.name}</span>
                            </div>
                        </summary>
                        <ul>{sub_menu}</ul>
                    </details>
                </li>
                '''

            elif item.is_link:
                if item.id in permission_list:
                    html += f'''
                        <li><a href='{item.url}' class="flex w-full">{item.name}</a></li>
                    '''
        return html


    def build_menu_hierarchy(menu_items):
        menu_dict = {}
        # Group menu items by their parent IDs
        for item in menu_items:
            if item.parent_id not in menu_dict:
                menu_dict[item.parent_id] = []
            menu_dict[item.parent_id].append(item)

        def build_tree(parent_id):
            # Recursive function to build tree structure
            children = menu_dict.get(parent_id, [])
            for child in children:
                child.children = build_tree(child.id)
            return children

        # Fetch root items (items with no parent)
        root_items = menu_dict.get(None, [])
        menu_hierarchy = []

        # Build tree structure starting from each root item
        for root_item in root_items:
            root_item.children = build_tree(root_item.id)
            menu_hierarchy.append(root_item)
        return menu_hierarchy

    if request.user.is_authenticated and request.path != '/':
        all_menu_items = MenuMaster.objects.filter(
            is_active=True, module__project__code = module_code
        ).order_by('parent__id', 'index', 'name')
        menu_hierarchy = build_menu_hierarchy(all_menu_items)
        menu_html = generate_menu_html(menu_hierarchy)

    return {
            'page_name' : str(request.resolver_match.url_name).replace('_', ' ').replace('page', '').capitalize(),
            'menu_name' : str(request.path.split('/')[1]).replace('-', ' '),
            'module_name' : str(settings.PROJECT_CODE).replace('is_', '').replace("_", " "),
            'module_name' : project.name,
            'menu_html' : menu_html
        }

