"""
3D Model işleme servisleri
Trimesh kütüphanesi kullanarak gerçek model işlemleri
"""
import trimesh
import numpy as np
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import tempfile


class ModelProcessor:
    """3D model işleme sınıfı"""
    
    def __init__(self, model_path):
        """Model yükle"""
        self.mesh = trimesh.load(model_path)
        self.original_mesh = self.mesh.copy()
    
    def cut_model(self, plane='xy', position=50, direction='above', tilt_x=0, tilt_y=0):
        """
        Modeli kes
        
        Args:
            plane: Kesme düzlemi ('xy', 'xz', 'yz')
            position: Kesme pozisyonu (0-100)
            direction: Hangi taraf kalacak ('above', 'below')
            tilt_x: X ekseninde eğim (derece)
            tilt_y: Y ekseninde eğim (derece)
        
        Returns:
            Kesilmiş mesh
        """
        # Mesh merkezini al
        bounds = self.mesh.bounds
        center = self.mesh.centroid
        
        # Kesme pozisyonunu hesapla
        normalized_pos = (position / 100) - 0.5  # -0.5 to 0.5
        
        # Düzlem normalini belirle
        if plane == 'xy':
            # Z ekseni boyunca kes
            plane_normal = np.array([0, 0, 1])
            plane_origin = center + np.array([0, 0, normalized_pos * (bounds[1][2] - bounds[0][2])])
        elif plane == 'xz':
            # Y ekseni boyunca kes
            plane_normal = np.array([0, 1, 0])
            plane_origin = center + np.array([0, normalized_pos * (bounds[1][1] - bounds[0][1]), 0])
        elif plane == 'yz':
            # X ekseni boyunca kes
            plane_normal = np.array([1, 0, 0])
            plane_origin = center + np.array([normalized_pos * (bounds[1][0] - bounds[0][0]), 0, 0])
        else:
            plane_normal = np.array([0, 1, 0])
            plane_origin = center
        
        # Eğim uygula
        if tilt_x != 0 or tilt_y != 0:
            # Eğim matrisini oluştur
            tilt_x_rad = np.radians(float(tilt_x))
            tilt_y_rad = np.radians(float(tilt_y))
            
            # X ekseni etrafında rotasyon
            if tilt_x != 0:
                rot_x = trimesh.transformations.rotation_matrix(tilt_x_rad, [1, 0, 0])
                plane_normal = trimesh.transformations.transform_points([plane_normal], rot_x)[0]
            
            # Y ekseni etrafında rotasyon
            if tilt_y != 0:
                rot_y = trimesh.transformations.rotation_matrix(tilt_y_rad, [0, 1, 0])
                plane_normal = trimesh.transformations.transform_points([plane_normal], rot_y)[0]
            
            # Normal vektörü normalize et
            plane_normal = plane_normal / np.linalg.norm(plane_normal)
        
        # Kesme yönünü belirle
        if direction == 'below':
            plane_normal = -plane_normal
        
        # Modeli kes
        try:
            sliced = self.mesh.slice_plane(
                plane_origin=plane_origin,
                plane_normal=plane_normal,
                cap=True  # Kesim yerini kapat
            )
            
            if sliced is not None and len(sliced.vertices) > 0:
                self.mesh = sliced
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Kesme hatası: {e}")
            return False
    
    def rotate_model(self, x_angle=0, y_angle=0, z_angle=0):
        """
        Modeli döndür
        
        Args:
            x_angle: X ekseni döndürme açısı (derece)
            y_angle: Y ekseni döndürme açısı (derece)
            z_angle: Z ekseni döndürme açısı (derece)
        """
        # Dereceleri radyana çevir
        x_rad = np.radians(float(x_angle))
        y_rad = np.radians(float(y_angle))
        z_rad = np.radians(float(z_angle))
        
        # Rotasyon matrislerini oluştur
        if x_rad != 0:
            matrix_x = trimesh.transformations.rotation_matrix(x_rad, [1, 0, 0])
            self.mesh.apply_transform(matrix_x)
        
        if y_rad != 0:
            matrix_y = trimesh.transformations.rotation_matrix(y_rad, [0, 1, 0])
            self.mesh.apply_transform(matrix_y)
        
        if z_rad != 0:
            matrix_z = trimesh.transformations.rotation_matrix(z_rad, [0, 0, 1])
            self.mesh.apply_transform(matrix_z)
        
        return True
    
    def smooth_model(self, iterations=5):
        """
        Modeli yumuşat (Laplacian smoothing)
        
        Args:
            iterations: İterasyon sayısı
        """
        try:
            # Trimesh'in smoothing fonksiyonu
            trimesh.smoothing.filter_laplacian(self.mesh, iterations=int(iterations))
            return True
        except Exception as e:
            print(f"Yumuşatma hatası: {e}")
            return False
    
    def fill_holes(self):
        """Model yüzeyindeki delikleri doldur"""
        try:
            self.mesh.fill_holes()
            return True
        except Exception as e:
            print(f"Delik doldurma hatası: {e}")
            return False
    
    def save_stl(self, output_path=None):
        """
        Modeli STL olarak kaydet
        
        Args:
            output_path: Kayıt yolu (None ise temp dosya)
        
        Returns:
            Dosya yolu
        """
        if output_path is None:
            # Geçici dosya oluştur
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.stl')
            output_path = temp_file.name
            temp_file.close()
        
        # STL olarak kaydet
        self.mesh.export(output_path)
        return output_path
    
    def get_stats(self):
        """Model istatistiklerini al"""
        return {
            'vertices_count': len(self.mesh.vertices),
            'faces_count': len(self.mesh.faces),
            'is_watertight': self.mesh.is_watertight,
            'volume': float(self.mesh.volume) if self.mesh.is_watertight else None,
            'surface_area': float(self.mesh.area),
            'bounds': self.mesh.bounds.tolist()
        }

