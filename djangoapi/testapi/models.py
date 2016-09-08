from django.db import models
        
class Disease(models.Model):
    Did		=	models.CharField(max_length=8,null=False,blank=False,unique=True,db_index=True)
    Name	=	models.CharField(max_length=128,null=False,blank=False,unique=False,db_index=True)
    Ename	=	models.CharField(max_length=128,null=True,blank=True,unique=False,db_index=False)
    Oname	=	models.CharField(max_length=1024,null=True,blank=True,unique=False,db_index=True)
    Dclass	=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=True)
    Icd10	=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=True)
    Icd9	=	models.CharField(max_length=4096,null=True,blank=True,unique=False,db_index=True)
    #seaweed
    Gs		=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Lxbx	=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    By		=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Fbjz	=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Lcbx	=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Bfz		=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Sysjc	=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Qtfzjc	=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Zd		=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Zxzd	=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Jbzd	=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Zl		=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Yh		=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Yf		=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
class Symptom(models.Model):
    Sid	= models.CharField(max_length=8,null=False,blank=False,unique=True,db_index=True)
    Name = models.CharField(max_length=64,null=False,blank=False,unique=False,db_index=True)
    Yjbw = models.CharField(max_length=64,null=True,blank=False,unique=False,db_index=True)
    Ejbw = models.CharField(max_length=64,null=True,blank=False,unique=False,db_index=True)
    Yjks = models.CharField(max_length=64,null=True,blank=False,unique=False,db_index=True)
    Ejks = models.CharField(max_length=64,null=True,blank=False,unique=False,db_index=True)
    #seaweed
    Zs = models.CharField(max_length=32,null=True,blank=True,unique=True,db_index=False)
    Zzxs = models.CharField(max_length=32,null=True,blank=True,unique=True,db_index=False)
    Zzqy = models.CharField(max_length=32,null=True,blank=True,unique=True,db_index=False)
    Dzyp = models.CharField(max_length=32,null=True,blank=True,unique=True,db_index=False)
    Knjb = models.CharField(max_length=32,null=True,blank=True,unique=True,db_index=False)
    Cyjc = models.CharField(max_length=32,null=True,blank=True,unique=True,db_index=False)
    Xszz = models.CharField(max_length=32,null=True,blank=True,unique=True,db_index=False)
    class Meta:
        unique_together = (("Sid","Name"),)
class Medication(models.Model):
    Mid	= models.CharField(max_length=8,null=False,blank=False,unique=True,db_index=True)
    Name = models.CharField(max_length=128,null=False,blank=False,unique=False,db_index=True)
    Ename = models.CharField(max_length=128,null=True,blank=True,unique=False,db_index=True)
    Oname = models.CharField(max_length=1024,null=True,blank=True,unique=False,db_index=True)
    Fclass = models.CharField(max_length=64,null=True,blank=True,unique=False,db_index=True)
    Sclass = models.CharField(max_length=64,null=True,blank=True,unique=False,db_index=True)
    Tclass = models.CharField(max_length=64,null=True,blank=True,unique=False,db_index=True)
    #seaweed
    Ywxyzy = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Ywjx = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Yfyl = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Ydx	= models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Jjz	= models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Syz	= models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Zysx = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Blfy = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Ylzy = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Zjdp = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    class Meta:
        unique_together = (("Mid","Name"),)

        
        
        
class Lab(models.Model):
    Lid	= models.CharField(max_length=8,null=False,blank=False,unique=True,db_index=True)
    Name = models.CharField(max_length=64,null=False,blank=False,unique=False,db_index=True)
    Ename = models.CharField(max_length=64,null=True,blank=True,unique=False,db_index=False)
    Oname = models.CharField(max_length=64,null=True,blank=True,unique=False,db_index=True)
    Fclass = models.CharField(max_length=64,null=True,blank=True,unique=False,db_index=True)
    Sclass = models.CharField(max_length=64,null=True,blank=True,unique=False,db_index=True)
    #seaweed
    Gs = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Yl = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Sj = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Czff = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Zcz = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Lcyy = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    Fz = models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False)
    class Meta:
        unique_together = (("Lid","Name"),)
        
        
class Image(models.Model):
    Iname	=	models.CharField(max_length=32,null=True,blank=True,unique=False,db_index=False) 
    Iid		=	models.CharField(max_length=8,null=False,blank=False,unique=True,db_index=True) 
    Fid		=	models.CharField(max_length=32,null=False,blank=False,unique=True,db_index=True)
