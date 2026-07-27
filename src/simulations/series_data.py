from datetime import datetime
from typing import Optional
from src.dtos.series.serie_response import SerieResponseDTO

serie_data: list[SerieResponseDTO] = [
    # 1. Breaking Bad - Drama
    SerieResponseDTO(
        id_serie=1,
        titulo='Breaking Bad',
        genero='Drama',
        año_inicio=2008,
        año_fin=2013,
        temporadas=5,
        episodios=62,                    
        estado='Finalizada',             
        sinopsis='Un profesor de química se convierte en fabricante de metanfetaminas.',  
        serie_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        serie_updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    
    # 2. Game of Thrones - Fantasía
    SerieResponseDTO(
        id_serie=2,
        titulo='Game of Thrones',
        genero='Fantasía',
        año_inicio=2011,
        año_fin=2019,
        temporadas=8,
        episodios=73,                    
        estado='Finalizada',             
        sinopsis='Nobles familias luchan por el control del Trono de Hierro.',  
        serie_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        serie_updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    
    # 3. The Office - Comedia
    SerieResponseDTO(
        id_serie=3,
        titulo='The Office',
        genero='Comedia',
        año_inicio=2005,
        año_fin=2013,
        temporadas=9,
        episodios=201,                   
        estado='Finalizada',             
        sinopsis='La vida en una oficina con un jefe excéntrico.',  
        serie_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        serie_updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    
    # 4. Stranger Things - Ciencia Ficción (en emisión)
    SerieResponseDTO(
        id_serie=4,
        titulo='Stranger Things',
        genero='Ciencia Ficción',
        año_inicio=2016,
        año_fin=None,                    # ← En emisión
        temporadas=4,
        episodios=34,                    
        estado='En emisión',             
        sinopsis='Un grupo de niños enfrenta misterios sobrenaturales en los 80.',  
        serie_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        serie_updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    
    # 5. The Crown - Drama Histórico
    SerieResponseDTO(
        id_serie=5,
        titulo='The Crown',
        genero='Drama Histórico',
        año_inicio=2016,
        año_fin=2023,
        temporadas=6,
        episodios=60,                    
        estado='Finalizada',             
        sinopsis='La vida de la Reina Isabel II a lo largo de las décadas.',  
        serie_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        serie_updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    
    # 6. The Last of Us - Drama (en emisión)
    SerieResponseDTO(
        id_serie=6,
        titulo='The Last of Us',
        genero='Drama',
        año_inicio=2023,
        año_fin=None,                    # ← En emisión
        temporadas=1,
        episodios=9,                     
        estado='En emisión',             
        sinopsis='Adaptación del videojuego en un mundo post-apocalíptico.',  
        serie_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        serie_updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    )
]