import logging
import sys


def factory(name, level='DEBUG'):
    """
    로거 인스턴스를 생성하고 설정하는 팩토리 함수
    
    Args:
        name (str): 로거 이름
        level (str): 로깅 레벨 (기본값: 'DEBUG')
    
    Returns:
        logging.Logger: 설정된 로거 인스턴스
    """
    # 로거 인스턴스 생성
    logger = logging.getLogger(name)
    
    # 표준 출력으로 로그를 출력하는 핸들러 생성
    handler = logging.StreamHandler(sys.stdout)
    
    # 로그 포맷 설정
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    )
    
    # 핸들러를 로거에 추가
    logger.addHandler(handler)
    
    # 로깅 레벨 설정
    logger.setLevel(getattr(logging, level))
    
    return logger
