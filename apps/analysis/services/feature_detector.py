"""
3D Model Özellik Tespit Servisi
Model yükleme, analiz ve özellik çıkarma
"""
import numpy as np
import trimesh
from typing import Dict, List, Any


class FeatureDetector:
    """3D model özelliklerini tespit eden sınıf"""
    
    def __init__(self, file_path: str):
        """
        Args:
            file_path: 3D model dosya yolu (.stl veya .ply)
        """
        self.file_path = file_path
        self.mesh = None
        self.load_mesh()
    
    def load_mesh(self):
        """Mesh dosyasını yükle"""
        try:
            self.mesh = trimesh.load(self.file_path)
            if isinstance(self.mesh, trimesh.Scene):
                # Eğer scene ise ilk geometry'yi al
                self.mesh = list(self.mesh.geometry.values())[0]
        except Exception as e:
            raise ValueError(f"Mesh yüklenemedi: {str(e)}")
    
    def analyze(self) -> Dict[str, Any]:
        """
        Tüm analizi yap ve sonuçları döndür
        
        Returns:
            Model analiz sonuçlarını içeren dictionary
        """
        if self.mesh is None:
            raise ValueError("Mesh yüklenmemiş")
        
        return {
            'vertices_count': len(self.mesh.vertices),
            'faces_count': len(self.mesh.faces),
            'is_watertight': self.mesh.is_watertight,
            'volume': float(self.mesh.volume) if self.mesh.is_watertight else None,
            'surface_area': float(self.mesh.area),
            'bounding_box': self.get_bounding_box(),
            'top_points': self.get_top_points(),
            'bottom_points': self.get_bottom_points(),
            'sharp_points': self.get_sharp_points(),
            'widest_area': self.get_widest_area(),
            'narrowest_area': self.get_narrowest_area(),
            'topology_status': self.check_topology()
        }
    
    def get_bounding_box(self) -> Dict:
        """Bounding box bilgilerini al"""
        bounds = self.mesh.bounds
        min_point = bounds[0].tolist()
        max_point = bounds[1].tolist()
        dimensions = (bounds[1] - bounds[0]).tolist()
        
        return {
            'min': min_point,
            'max': max_point,
            'dimensions': dimensions
        }
    
    def get_top_points(self, n=5) -> List[Dict]:
        """
        En üst noktaları bul
        
        Args:
            n: Bulunacak nokta sayısı
            
        Returns:
            En yüksek n noktanın listesi
        """
        vertices = self.mesh.vertices
        # Y ekseninde en yüksek noktalar
        sorted_indices = np.argsort(vertices[:, 1])[-n:]
        
        top_points = []
        for idx in sorted_indices:
            point = vertices[idx]
            top_points.append({
                'x': float(point[0]),
                'y': float(point[1]),
                'z': float(point[2])
            })
        
        return top_points
    
    def get_bottom_points(self, n=5) -> List[Dict]:
        """
        En alt noktaları bul
        
        Args:
            n: Bulunacak nokta sayısı
            
        Returns:
            En alçak n noktanın listesi
        """
        vertices = self.mesh.vertices
        # Y ekseninde en düşük noktalar
        sorted_indices = np.argsort(vertices[:, 1])[:n]
        
        bottom_points = []
        for idx in sorted_indices:
            point = vertices[idx]
            bottom_points.append({
                'x': float(point[0]),
                'y': float(point[1]),
                'z': float(point[2])
            })
        
        return bottom_points
    
    def get_sharp_points(self, curvature_threshold=0.7, max_points=20) -> List[Dict]:
        """
        Sivri noktaları tespit et (yüksek eğrilik)
        
        Args:
            curvature_threshold: Eğrilik eşiği (0-1 arası)
            max_points: Maksimum nokta sayısı
            
        Returns:
            Sivri noktaların listesi
        """
        try:
            # Vertex normal'lerini hesapla
            vertex_normals = self.mesh.vertex_normals
            
            # Her vertex için komşu vertex'lerin normallerini karşılaştır
            # Büyük normal farkları = yüksek eğrilik = sivri nokta
            curvatures = []
            
            for i, vertex in enumerate(self.mesh.vertices):
                # Yakın vertex'leri bul (basit yaklaşım)
                distances = np.linalg.norm(self.mesh.vertices - vertex, axis=1)
                neighbors = np.where(distances < np.percentile(distances, 5))[0]
                
                if len(neighbors) > 1:
                    # Komşu normal'lerin varyansını hesapla
                    neighbor_normals = vertex_normals[neighbors]
                    variance = np.mean(np.abs(neighbor_normals - vertex_normals[i]))
                    curvatures.append((i, float(variance)))
            
            # En yüksek eğriliğe sahip noktaları seç
            curvatures.sort(key=lambda x: x[1], reverse=True)
            sharp_indices = [idx for idx, curv in curvatures[:max_points] if curv > curvature_threshold]
            
            sharp_points = []
            for idx in sharp_indices:
                point = self.mesh.vertices[idx]
                sharp_points.append({
                    'x': float(point[0]),
                    'y': float(point[1]),
                    'z': float(point[2]),
                    'curvature': curvatures[idx][1] if idx < len(curvatures) else 0
                })
            
            return sharp_points[:max_points]
            
        except Exception as e:
            print(f"Sivri nokta tespitinde hata: {e}")
            return []
    
    def get_widest_area(self) -> Dict:
        """En geniş alanı bul"""
        bounds = self.mesh.bounds
        dimensions = bounds[1] - bounds[0]
        
        # En geniş ekseni bul
        widest_axis = np.argmax(dimensions)
        axis_names = ['x', 'y', 'z']
        
        center = self.mesh.centroid
        
        return {
            'position': {
                'x': float(center[0]),
                'y': float(center[1]),
                'z': float(center[2])
            },
            'width': float(dimensions[widest_axis]),
            'direction': axis_names[widest_axis]
        }
    
    def get_narrowest_area(self) -> Dict:
        """En dar alanı bul"""
        bounds = self.mesh.bounds
        dimensions = bounds[1] - bounds[0]
        
        # En dar ekseni bul
        narrowest_axis = np.argmin(dimensions)
        axis_names = ['x', 'y', 'z']
        
        center = self.mesh.centroid
        
        return {
            'position': {
                'x': float(center[0]),
                'y': float(center[1]),
                'z': float(center[2])
            },
            'width': float(dimensions[narrowest_axis]),
            'direction': axis_names[narrowest_axis]
        }
    
    def check_topology(self) -> str:
        """
        Topoloji durumunu kontrol et
        
        Returns:
            'good', 'has_holes', 'non_manifold', 'complex'
        """
        # Watertight kontrolü
        if not self.mesh.is_watertight:
            return 'has_holes'
        
        # Manifold kontrolü
        if not self.mesh.is_winding_consistent:
            return 'non_manifold'
        
        # Euler characteristic kontrolü (topolojik karmaşıklık)
        euler = self.mesh.euler_number
        
        # Basit kapalı mesh için euler = 2 olmalı
        if euler == 2:
            return 'good'
        else:
            return 'complex'
    
    def get_visualization_data(self) -> Dict:
        """3D görselleştirme için veri hazırla"""
        return {
            'vertices': self.mesh.vertices.tolist(),
            'faces': self.mesh.faces.tolist(),
            'normals': self.mesh.vertex_normals.tolist(),
            'centroid': self.mesh.centroid.tolist(),
            'bounds': self.mesh.bounds.tolist()
        }


