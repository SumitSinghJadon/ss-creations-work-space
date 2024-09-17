from urllib import response
from PIL import Image, ImageFilter
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token # Add By Sudhir
from IS_Nexus.functions.data_conversion import queryset_to_json
import json
from django.core.files.uploadedfile import InMemoryUploadedFile
import random
from QMS_db.models.style_silhouettes import StyleSilhouettes
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image, ImageFilter
import os
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class QmsDefectView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def create_sketch(self, image):
        try:
            img = Image.open(image)
            
            # Convert image to grayscale
            gray_image = img.convert('L')
            
            # Apply Gaussian blur to the grayscale image
            blurred_image = gray_image.filter(ImageFilter.GaussianBlur(radius=0.8))
            
            # Perform edge detection
            edge_image = blurred_image.filter(ImageFilter.FIND_EDGES)
            
            # Create a new image with white background
            white_background = Image.new('RGB', img.size, (255, 255, 255))
            
            # Composite the edge image onto the white background using the alpha mask
            final_image = Image.composite(edge_image, white_background, edge_image)
            
            return final_image
        
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    def post(self, request):
        if request.method == 'POST' and request.FILES.get('image'):
            try:
                original_image = request.FILES['image']
                sketch_image = self.create_sketch(original_image)
                
                if sketch_image:
                    sketch_image_name = os.path.splitext(original_image.name)[0] + '_sketch.png'
                    sketch_image_path = os.path.join(settings.MEDIA_ROOT, 'sketches', sketch_image_name)
                    
                    os.makedirs(os.path.dirname(sketch_image_path), exist_ok=True)
                    sketch_image.save(sketch_image_path)
                    sketch_image_url = os.path.join(settings.MEDIA_URL, 'sketches', sketch_image_name)
                    
                    return JsonResponse({'sketch_image_url': sketch_image_url})
                else:
                    return JsonResponse({'error': 'Failed to process image.'}, status=400)
                
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        
        return JsonResponse({'error': 'No image provided.'}, status=400)



# class StyleSilhouettesView(View):
    
#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
    
#     def post(self, request):
#         try:
#             if request.method == 'POST' and request.FILES.get('front_image'):
#                 data = json.loads(request.body.decode('utf-8'))
#                 print(data)
#                 front_image = request.FILES.get('front_image')
#                 back_image = request.FILES.get('back_image')
#                 buyer = data.get('buyer')
#                 style_no = data.get('style_no')
                
#                 if front_image and back_image and buyer and style_no:
#                     silhouette = StyleSilhouettes(
#                         front_image=front_image,
#                         back_image=back_image,
#                         buyer=buyer,
#                         style_no=style_no
#                     )
                    
#                     silhouette.full_clean()  # Validate model fields
                    
#                     silhouette.save()
                    
#                     return JsonResponse({'success': 'Silhouette saved successfully.'}, status=201)
#             else:
#                 return JsonResponse({'error': 'Missing required fields or files.'}, status=400)
        
#         except ValidationError as ve:
#             return JsonResponse({'error': ve.message_dict}, status=400)
        
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)




from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

@method_decorator(csrf_exempt, name='dispatch')
class StyleSilhouettesView(View):
    def post(self, request, *args, **kwargs):
        front_image = request.POST.get('front_image')
        back_image = request.POST.get('back_image')
        buyer = request.POST.get('buyer')
        style_no = request.POST.get('style_no')
        # print(front_image,back_image,buyer,style_no)

        style_silhouette = StyleSilhouettes(
            front_image=front_image,
            back_image=back_image,
            buyer=buyer,
            style_no=style_no
        )

        try:
            style_silhouette.save()
            return JsonResponse({'message': 'Data saved successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        

        
    def get(self, request):
        buyer = request.GET.get('buyer')
        style_no = request.GET.get('styleno')
        queryset = StyleSilhouettes.objects.filter(buyer=buyer, style_no=style_no).values()
        list_data_silhouettes = list(queryset)
        return JsonResponse(list_data_silhouettes, content_type='application/json',safe=False)
  