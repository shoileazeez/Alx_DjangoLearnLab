from models import Book
create_instances = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
create_instances.save()

# with open('instance.py') as f:
#     exec(f.read())
# with open('C:\Users\Admin\Alx_DjangoLearnLab\0x1.Introduction_ to_ Django\LibraryProject\bookshelf\instance.py') as f:
#     exec(f.read())
    
