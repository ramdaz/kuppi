from PIL import Image, ImageOps, ImageDraw
import os, random
import sys
    
def get_name(image):
    if os.path.exists(image):
	name, ext=os.path.splitext(image)
    if ext.lower() in (".jpg", ".png", ".jpeg"):
	newname= name+"_avatar"
	return newname
    return None
def get_output_name(image, size):
    if get_name(image) !=None:
	new_image = get_name(image) +"_"+str(size[0]) +"_"+str(size[1])+".png"
	return new_image
    else:
	return None
def transparenter(image):
    img = Image.open(image)
    img = img.convert("RGBA")

    pixdata = img.load()

    for y in xrange(img.size[1]):
	for x in xrange(img.size[0]):
	    if pixdata[x, y] == (255, 255, 255, 255):
		pixdata[x, y] = (255, 255, 255, 0)
    img.save(image, "PNG")
def masker(image, size=None):

    new_name = get_name(image)
    if new_name !=None:
	pass
    else:
	return None
    if size==None:
	size= (128, 128)
    
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + size, fill=255)
    im = Image.open(image)
    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    new_image = new_name +"_"+str(size[0]) +"_"+str(size[1])+".png"
    output.save(new_image)
    transparenter(new_image)
    print "New Image Saved %s" % str(new_image)
    return new_image


'''
if __name__=="__main__":
    if len(sys.argv) in 1,3:
	pass
    else:
	print "Pass the image and a tuple seperated by space\n like shah.jpg 128 128"
    if len(sys.argv)==1:
	masker(sys.argv[0])
    elif len(sys.argv)==2:
	masker(sys.argv[0], (sys.argv[1], sys.argv[2]))
'''
